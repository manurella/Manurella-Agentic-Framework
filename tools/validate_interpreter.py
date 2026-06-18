"""Validate Interpreter Task Frames, Acceptance Contracts, and fixture projections."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
import json
import pathlib
import sys
from typing import Any, Iterable

import yaml

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("jsonschema is required to validate Interpreter contracts") from exc


TASK_FRAME_SCHEMA = pathlib.Path("schemas/interpreter/task-frame.schema.json")
ACCEPTANCE_SCHEMA = pathlib.Path("schemas/interpreter/acceptance-contract.schema.json")
DEFAULT_FIXTURE_DIR = pathlib.Path("evals/fixtures/interpreter")

UNCERTAINTY_KINDS = {
    "ambiguities": "ambiguity",
    "assumptions": "assumption",
    "missing_information": "missing",
    "contradictions": "contradiction",
}
BLOCKING_IMPACTS = {"material", "consequential"}
BLOCKING_ACTIONS = {"ask", "confirm", "refuse"}
PROCEED_ACTIONS = {"proceed", "proceed_with_assumption"}
MUTATING_WORK_TYPES = {"create", "transform", "act"}
CONSEQUENTIAL_LEVELS = {"consequential", "critical"}
ACTIVE_UNCERTAINTY_STATUSES = {"open", "accepted_for_now"}
FRESHNESS_RANK = {"stable": 0, "current": 1, "real_time": 2}


@dataclass(frozen=True)
class Issue:
    code: str
    path: str
    message: str

    def render(self) -> str:
        location = f" at {self.path}" if self.path else ""
        return f"{self.code}{location}: {self.message}"


def load_mapping(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def set_dotted_value(data: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = dotted_path.split(".")
    target: dict[str, Any] = data
    for part in parts[:-1]:
        child = target.get(part)
        if not isinstance(child, dict):
            raise ValueError(f"mutation path does not resolve to a mapping: {dotted_path}")
        target = child
    target[parts[-1]] = value


def materialize_fixture(path: pathlib.Path, data: dict[str, Any]) -> dict[str, Any]:
    """Apply a focused negative-fixture mutation to a complete positive fixture."""

    base_ref = data.get("base_fixture")
    if base_ref is None:
        return data
    if not isinstance(base_ref, str) or not base_ref:
        raise ValueError("base_fixture must be a non-empty relative path")
    base_path = (path.parent / base_ref).resolve()
    base = load_mapping(base_path)
    if "base_fixture" in base:
        raise ValueError("nested base_fixture inheritance is not supported")

    result = copy.deepcopy(base)
    for key in (
        "fixture_id",
        "scenario",
        "expected_validation",
        "expected_error_codes",
        "expected_projection",
    ):
        if key in data:
            result[key] = copy.deepcopy(data[key])

    mutations = data.get("mutations")
    if not isinstance(mutations, list) or not mutations:
        raise ValueError("derived fixture requires at least one mutation")
    for mutation in mutations:
        if not isinstance(mutation, dict) or set(mutation) != {"path", "value"}:
            raise ValueError("each mutation must contain exactly path and value")
        dotted_path = mutation.get("path")
        if not isinstance(dotted_path, str) or not dotted_path:
            raise ValueError("mutation path must be a non-empty string")
        set_dotted_value(result, dotted_path, copy.deepcopy(mutation.get("value")))
    return result


def load_json_schema(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load schema {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"schema {path} must contain an object")
    Draft202012Validator.check_schema(data)
    return data


def json_path(parts: Iterable[Any], prefix: str) -> str:
    path = prefix
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def schema_issues(
    instance: Any,
    validator: Draft202012Validator,
    prefix: str,
) -> list[Issue]:
    issues: list[Issue] = []
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    for error in errors:
        issues.append(
            Issue(
                code=f"schema.{error.validator}",
                path=json_path(error.absolute_path, prefix),
                message=error.message,
            )
        )
    return issues


def versioned_ref(identifier: str, version: int) -> str:
    return f"{identifier}@{version}"


def uncertainty_items(task_frame: dict[str, Any]) -> list[dict[str, Any]]:
    uncertainty = task_frame.get("uncertainty")
    if not isinstance(uncertainty, dict):
        return []
    items: list[dict[str, Any]] = []
    for section in UNCERTAINTY_KINDS:
        values = uncertainty.get(section)
        if isinstance(values, list):
            items.extend(value for value in values if isinstance(value, dict))
    return items


def blocking_uncertainty(task_frame: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in uncertainty_items(task_frame)
        if item.get("status") == "open" and item.get("impact") in BLOCKING_IMPACTS
    ]


def project_family_class(task_frame: dict[str, Any]) -> str:
    """Derive the legacy Family A-E label without replacing Task Frame dimensions."""

    if blocking_uncertainty(task_frame):
        return "E"

    objective = task_frame.get("objective") or {}
    scope = task_frame.get("scope") or {}
    work_types = set(objective.get("work_types") or [])
    if work_types == {"converse"}:
        return "D"
    if scope.get("horizon") == "project":
        return "C"

    outcomes = objective.get("desired_outcomes") or []
    artifacts = scope.get("artifacts") or []
    dependencies = scope.get("dependencies") or []
    if scope.get("horizon") == "session" or len(outcomes) > 1 or len(artifacts) > 1 or dependencies:
        return "B"
    return "A"


def project_posture(task_frame: dict[str, Any]) -> str | None:
    scope = task_frame.get("scope")
    if not isinstance(scope, dict):
        return None
    value = scope.get("project_posture")
    return value if isinstance(value, str) else None


def validate_clarification_shape(decision: Any) -> list[Issue]:
    if not isinstance(decision, dict):
        return [Issue("semantic.clarification_shape", "clarification_decision", "must be a mapping")]

    issues: list[Issue] = []
    required = {
        "action",
        "reasons",
        "affected_uncertainty_ids",
        "question",
        "options",
        "blocks_execution",
    }
    missing = sorted(required - set(decision))
    if missing:
        issues.append(
            Issue(
                "semantic.clarification_shape",
                "clarification_decision",
                f"missing fields: {', '.join(missing)}",
            )
        )
        return issues

    action = decision.get("action")
    if action not in BLOCKING_ACTIONS | PROCEED_ACTIONS:
        issues.append(
            Issue(
                "semantic.clarification_action",
                "clarification_decision.action",
                f"unknown action: {action!r}",
            )
        )
    for field in ("reasons", "affected_uncertainty_ids", "options"):
        value = decision.get(field)
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            issues.append(
                Issue(
                    "semantic.clarification_shape",
                    f"clarification_decision.{field}",
                    "must be an array of non-empty strings",
                )
            )
    question = decision.get("question")
    if question is not None and (not isinstance(question, str) or not question):
        issues.append(
            Issue(
                "semantic.clarification_shape",
                "clarification_decision.question",
                "must be a non-empty string or null",
            )
        )
    if not isinstance(decision.get("blocks_execution"), bool):
        issues.append(
            Issue(
                "semantic.clarification_shape",
                "clarification_decision.blocks_execution",
                "must be a boolean",
            )
        )
    return issues


def validate_semantics(
    task_frame: dict[str, Any],
    acceptance: dict[str, Any],
    clarification: dict[str, Any],
) -> list[Issue]:
    issues: list[Issue] = []
    identity = task_frame.get("identity") or {}
    objective = task_frame.get("objective") or {}
    scope = task_frame.get("scope") or {}
    governance = task_frame.get("governance") or {}
    provenance = task_frame.get("provenance") or {}
    lifecycle = task_frame.get("lifecycle") or {}

    frame_id = identity.get("frame_id")
    frame_version = identity.get("version")
    contract_id = acceptance.get("contract_id")
    contract_version = acceptance.get("version")
    if isinstance(frame_id, str) and isinstance(frame_version, int):
        expected_frame_ref = versioned_ref(frame_id, frame_version)
        if acceptance.get("task_frame_ref") != expected_frame_ref:
            issues.append(
                Issue(
                    "semantic.reference_mismatch",
                    "acceptance_contract.task_frame_ref",
                    f"must equal {expected_frame_ref!r}",
                )
            )
    if isinstance(contract_id, str) and isinstance(contract_version, int):
        expected_contract_ref = versioned_ref(contract_id, contract_version)
        if task_frame.get("acceptance_contract_ref") != expected_contract_ref:
            issues.append(
                Issue(
                    "semantic.reference_mismatch",
                    "task_frame.acceptance_contract_ref",
                    f"must equal {expected_contract_ref!r}",
                )
            )
    if isinstance(frame_version, int) and isinstance(contract_version, int) and frame_version != contract_version:
        issues.append(
            Issue(
                "semantic.version_mismatch",
                "acceptance_contract.version",
                "must match the Task Frame version",
            )
        )

    parent_frame_id = identity.get("parent_frame_id")
    root_frame_id = identity.get("root_frame_id")
    if parent_frame_id is None and frame_id and root_frame_id != frame_id:
        issues.append(
            Issue(
                "semantic.root_lineage",
                "task_frame.identity.root_frame_id",
                "a root frame must reference its own frame_id",
            )
        )
    if parent_frame_id is not None and root_frame_id == frame_id:
        issues.append(
            Issue(
                "semantic.root_lineage",
                "task_frame.identity.root_frame_id",
                "a child frame must reference the shared root frame",
            )
        )

    supersedes = provenance.get("supersedes_frame_ref")
    changed_fields = provenance.get("changed_fields") or []
    invalidated_outputs = provenance.get("invalidated_outputs") or []
    if frame_version == 1 and (supersedes is not None or changed_fields or invalidated_outputs):
        issues.append(
            Issue(
                "semantic.revision_lineage",
                "task_frame.provenance",
                "version 1 cannot supersede or invalidate an earlier frame",
            )
        )
    if isinstance(frame_version, int) and frame_version > 1:
        expected_previous = versioned_ref(str(frame_id), frame_version - 1)
        if supersedes != expected_previous or not changed_fields:
            issues.append(
                Issue(
                    "semantic.revision_lineage",
                    "task_frame.provenance",
                    f"a revision must supersede {expected_previous!r} and name changed_fields",
                )
            )

    if scope.get("horizon") == "project":
        if identity.get("project_id") is None or scope.get("project_posture") is None:
            issues.append(
                Issue(
                    "semantic.project_context",
                    "task_frame.scope",
                    "project horizon requires project_id and project_posture",
                )
            )

    uncertainty = task_frame.get("uncertainty") or {}
    known_uncertainty_ids: set[str] = set()
    for section, expected_kind in UNCERTAINTY_KINDS.items():
        values = uncertainty.get(section) or []
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if isinstance(item_id, str):
                if item_id in known_uncertainty_ids:
                    issues.append(
                        Issue(
                            "semantic.duplicate_uncertainty_id",
                            f"task_frame.uncertainty.{section}[{index}].id",
                            f"duplicate uncertainty id {item_id!r}",
                        )
                    )
                known_uncertainty_ids.add(item_id)
            if item.get("kind") != expected_kind:
                issues.append(
                    Issue(
                        "semantic.uncertainty_kind",
                        f"task_frame.uncertainty.{section}[{index}].kind",
                        f"must be {expected_kind!r}",
                    )
                )
            if item.get("status") in ACTIVE_UNCERTAINTY_STATUSES and item.get("resolution") is not None:
                issues.append(
                    Issue(
                        "semantic.uncertainty_resolution",
                        f"task_frame.uncertainty.{section}[{index}].resolution",
                        "active uncertainty cannot already have a resolution",
                    )
                )
            if item.get("status") in {"resolved", "user_confirmed", "invalidated"} and item.get("resolution") is None:
                issues.append(
                    Issue(
                        "semantic.uncertainty_resolution",
                        f"task_frame.uncertainty.{section}[{index}].resolution",
                        "closed uncertainty requires a resolution",
                    )
                )

    blocking = blocking_uncertainty(task_frame)
    clarity = scope.get("clarity")
    if blocking and clarity not in {"ambiguous", "contradictory"}:
        issues.append(
            Issue(
                "semantic.executable_has_blocking_uncertainty",
                "task_frame.scope.clarity",
                "open material or consequential uncertainty cannot be executable or safely inferable",
            )
        )
    if not blocking and clarity in {"ambiguous", "contradictory"}:
        issues.append(
            Issue(
                "semantic.ambiguity_without_blocker",
                "task_frame.scope.clarity",
                "ambiguous or contradictory framing requires open material uncertainty",
            )
        )

    clarification_issues = validate_clarification_shape(clarification)
    issues.extend(clarification_issues)
    if not clarification_issues:
        action = clarification.get("action")
        blocks_execution = clarification.get("blocks_execution")
        if (action in BLOCKING_ACTIONS) != blocks_execution:
            issues.append(
                Issue(
                    "semantic.clarification_blocking",
                    "clarification_decision.blocks_execution",
                    "ask, confirm, and refuse must block; proceed actions must not block",
                )
            )
        if action in {"ask", "confirm"} and not clarification.get("question"):
            issues.append(
                Issue(
                    "semantic.clarification_question",
                    "clarification_decision.question",
                    "ask and confirm require one grouped question",
                )
            )
        if action == "proceed_with_assumption" and not any(
            item.get("kind") == "assumption" and item.get("status") == "accepted_for_now"
            for item in uncertainty_items(task_frame)
        ):
            issues.append(
                Issue(
                    "semantic.assumption_missing",
                    "clarification_decision.action",
                    "proceed_with_assumption requires a recorded accepted_for_now assumption",
                )
            )
        unknown_ids = set(clarification.get("affected_uncertainty_ids") or []) - known_uncertainty_ids
        if unknown_ids:
            issues.append(
                Issue(
                    "semantic.unknown_uncertainty_ref",
                    "clarification_decision.affected_uncertainty_ids",
                    f"unknown uncertainty ids: {', '.join(sorted(unknown_ids))}",
                )
            )
        family_class = project_family_class(task_frame)
        if family_class == "E" and (action not in BLOCKING_ACTIONS or not blocks_execution):
            issues.append(
                Issue(
                    "semantic.family_e_must_block",
                    "clarification_decision",
                    "Family E requires an ask, confirm, or refusal before execution",
                )
            )
        if (lifecycle.get("status") == "awaiting_clarification") != blocks_execution:
            issues.append(
                Issue(
                    "semantic.lifecycle_clarification",
                    "task_frame.lifecycle.status",
                    "awaiting_clarification must match a blocking clarification decision",
                )
            )

    consequence = governance.get("consequence")
    reversibility = governance.get("reversibility")
    confirmations = governance.get("confirmations_required") or []
    if consequence in CONSEQUENTIAL_LEVELS or reversibility == "irreversible":
        if not confirmations:
            issues.append(
                Issue(
                    "semantic.confirmation_required",
                    "task_frame.governance.confirmations_required",
                    "consequential, critical, or irreversible work requires confirmation",
                )
            )
        if acceptance.get("control", {}).get("signoff_required") is not True:
            issues.append(
                Issue(
                    "semantic.signoff_required",
                    "acceptance_contract.control.signoff_required",
                    "consequential, critical, or irreversible work requires signoff",
                )
            )

    work_types = set(objective.get("work_types") or [])
    if "act" in work_types and objective.get("autonomy") in {"execute", "execute_with_approval"}:
        if not governance.get("permissions_required"):
            issues.append(
                Issue(
                    "semantic.permission_required",
                    "task_frame.governance.permissions_required",
                    "executed external action requires an explicit permission record",
                )
            )

    if scope.get("project_posture") == "audit" and work_types & MUTATING_WORK_TYPES:
        issues.append(
            Issue(
                "semantic.audit_mutation",
                "task_frame.objective.work_types",
                "audit posture cannot create, transform, or act",
            )
        )

    task_freshness = task_frame.get("constraints", {}).get("freshness")
    evidence_freshness = acceptance.get("evidence_requirements", {}).get("freshness")
    if task_freshness in FRESHNESS_RANK and evidence_freshness in FRESHNESS_RANK:
        if FRESHNESS_RANK[evidence_freshness] < FRESHNESS_RANK[task_freshness]:
            issues.append(
                Issue(
                    "semantic.freshness_downgrade",
                    "acceptance_contract.evidence_requirements.freshness",
                    "evidence freshness cannot be weaker than the Task Frame requirement",
                )
            )

    dimensions = acceptance.get("quality_rubric", {}).get("dimensions") or []
    dimension_ids = {item.get("id") for item in dimensions if isinstance(item, dict)}
    critical_ids = set(acceptance.get("quality_rubric", {}).get("critical_dimensions") or [])
    unknown_critical = critical_ids - dimension_ids
    if unknown_critical:
        issues.append(
            Issue(
                "semantic.unknown_critical_dimension",
                "acceptance_contract.quality_rubric.critical_dimensions",
                f"unknown rubric dimensions: {', '.join(sorted(unknown_critical))}",
            )
        )
    declared_critical = {
        item.get("id")
        for item in dimensions
        if isinstance(item, dict) and item.get("critical") is True
    }
    if declared_critical != critical_ids:
        issues.append(
            Issue(
                "semantic.critical_dimension_mismatch",
                "acceptance_contract.quality_rubric",
                "critical_dimensions must exactly match dimensions marked critical",
            )
        )
    if dimensions:
        total_weight = sum(
            float(item.get("weight", 0)) for item in dimensions if isinstance(item, dict)
        )
        if abs(total_weight - 1.0) > 0.000001:
            issues.append(
                Issue(
                    "semantic.rubric_weight",
                    "acceptance_contract.quality_rubric.dimensions",
                    f"rubric weights must total 1.0, got {total_weight:g}",
                )
            )
    return issues


def validate_bundle(
    data: dict[str, Any],
    task_validator: Draft202012Validator,
    acceptance_validator: Draft202012Validator,
) -> list[Issue]:
    task_frame = data.get("task_frame")
    acceptance = data.get("acceptance_contract")
    clarification = data.get("clarification_decision")
    issues = schema_issues(task_frame, task_validator, "task_frame")
    issues.extend(schema_issues(acceptance, acceptance_validator, "acceptance_contract"))
    issues.extend(validate_clarification_shape(clarification))
    if issues:
        return issues
    return validate_semantics(task_frame, acceptance, clarification)


def run_fixture_suite(
    fixture_dir: pathlib.Path,
    task_validator: Draft202012Validator,
    acceptance_validator: Draft202012Validator,
) -> int:
    paths = sorted([*fixture_dir.rglob("*.yaml"), *fixture_dir.rglob("*.yml")])
    if not paths:
        print(f"error: no Interpreter fixtures found under {fixture_dir}", file=sys.stderr)
        return 1

    failures = 0
    for path in paths:
        try:
            data = materialize_fixture(path, load_mapping(path))
        except ValueError as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failures += 1
            continue

        issues = validate_bundle(data, task_validator, acceptance_validator)
        actual = "fail" if issues else "pass"
        expected = data.get("expected_validation", "pass")
        expected_codes = set(data.get("expected_error_codes") or [])
        actual_codes = {issue.code for issue in issues}
        projection = {
            "family_class": project_family_class(data.get("task_frame") or {}),
            "project_posture": project_posture(data.get("task_frame") or {}),
        }
        expected_projection = data.get("expected_projection")

        mismatch = actual != expected
        if expected == "fail" and actual_codes != expected_codes:
            mismatch = True
        if expected_projection is not None and projection != expected_projection:
            mismatch = True

        relative = path.as_posix()
        if mismatch:
            failures += 1
            print(f"FAIL {relative}: expected {expected}, got {actual}", file=sys.stderr)
            if expected_codes - actual_codes:
                print(
                    f"  missing expected error codes: {', '.join(sorted(expected_codes - actual_codes))}",
                    file=sys.stderr,
                )
            if actual_codes - expected_codes:
                print(
                    f"  unexpected error codes: {', '.join(sorted(actual_codes - expected_codes))}",
                    file=sys.stderr,
                )
            if expected_projection is not None and projection != expected_projection:
                print(
                    f"  projection mismatch: expected {expected_projection}, got {projection}",
                    file=sys.stderr,
                )
            for issue in issues:
                print(f"  {issue.render()}", file=sys.stderr)
        else:
            print(
                f"PASS {relative}: validation={actual}, family={projection['family_class']}, "
                f"posture={projection['project_posture'] or 'none'}"
            )

    if failures:
        print(f"Interpreter fixture validation failed: {failures}/{len(paths)} case(s)")
        return 1
    print(f"Interpreter fixture validation passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path, help="validate one Interpreter bundle")
    parser.add_argument(
        "--fixture-dir",
        type=pathlib.Path,
        default=DEFAULT_FIXTURE_DIR,
        help="fixture directory used when --input is omitted",
    )
    return parser.parse_args(argv)


def resolve_under(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        task_schema = load_json_schema(root / TASK_FRAME_SCHEMA)
        acceptance_schema = load_json_schema(root / ACCEPTANCE_SCHEMA)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    format_checker = FormatChecker()
    task_validator = Draft202012Validator(task_schema, format_checker=format_checker)
    acceptance_validator = Draft202012Validator(acceptance_schema, format_checker=format_checker)

    if args.input:
        input_path = resolve_under(root, args.input)
        try:
            data = load_mapping(input_path)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        issues = validate_bundle(data, task_validator, acceptance_validator)
        for issue in issues:
            print(f"error: {issue.render()}", file=sys.stderr)
        if issues:
            print(f"Interpreter validation failed: {len(issues)} issue(s)")
            return 1
        print(
            "Interpreter validation passed: "
            f"family={project_family_class(data['task_frame'])}, "
            f"posture={project_posture(data['task_frame']) or 'none'}"
        )
        return 0

    fixture_dir = resolve_under(root, args.fixture_dir)
    return run_fixture_suite(fixture_dir, task_validator, acceptance_validator)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
