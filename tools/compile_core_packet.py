"""Compile a validated Interpreter bundle into a Core routing decision."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
import yaml

from validate_interpreter import (
    ACCEPTANCE_SCHEMA,
    DEFAULT_FIXTURE_DIR,
    TASK_FRAME_SCHEMA,
    load_json_schema,
    load_mapping,
    materialize_fixture,
    project_family_class,
    project_posture,
    validate_bundle,
    versioned_ref,
)


ROUTING_SCHEMA = pathlib.Path("schemas/core/routing-decision.schema.json")
DOMAIN_AGENTS = {
    "core": "manurella-orchestrator",
    "build": "build-orchestrator",
    "muse": "muse-lead",
    "pixel": "pixel-director",
    "mentor": "macro-placement-director",
}
SPECIALIST_DOMAINS = ("build", "muse", "pixel", "mentor")
BANNED_PROJECTION_KEYS = {"raw_request", "turn_refs", "untrusted_data_refs"}

DOMAIN_SIGNALS = {
    "build": {
        "architecture",
        "build",
        "code",
        "documentation_edit",
        "frontend",
        "implementation",
        "markdown",
        "repository",
        "software",
        "software-system",
        "testing",
    },
    "muse": {
        "copy",
        "creative_writing",
        "editing",
        "line_editing",
        "narrative",
        "prose",
        "scene",
        "story",
    },
    "pixel": {
        "art_direction",
        "image",
        "image-prompt",
        "prompt_compilation",
        "visual",
        "visual-generation",
    },
    "mentor": {
        "curriculum",
        "interview_study",
        "learn",
        "learning",
        "teaching",
        "tutoring",
    },
}


class ProjectionError(ValueError):
    pass


def unique_strings(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def criterion_statements(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    return [
        item["statement"]
        for item in items
        if isinstance(item, dict) and isinstance(item.get("statement"), str)
    ]


def check_descriptions(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    return [
        item["description"]
        for item in items
        if isinstance(item, dict) and isinstance(item.get("description"), str)
    ]


def routing_signal_values(task_frame: dict[str, Any]) -> list[str]:
    scope = task_frame["scope"]
    hints = task_frame["routing_hints"]
    values = [str(value).lower() for value in hints["required_capabilities"]]
    values.extend(str(item["kind"]).lower() for item in scope["artifacts"])
    values.extend(str(value).lower() for value in task_frame["objective"]["work_types"])
    return values


def select_domain(task_frame: dict[str, Any]) -> tuple[str, list[str]]:
    candidates = task_frame["routing_hints"]["candidate_domains"]
    unknown = [candidate for candidate in candidates if candidate not in DOMAIN_AGENTS]
    if unknown:
        raise ProjectionError(f"unsupported candidate domains: {', '.join(unknown)}")

    specialists = [candidate for candidate in candidates if candidate in SPECIALIST_DOMAINS]
    if not specialists:
        if "core" in candidates:
            return "core", []
        raise ProjectionError("executable Task Frame has no supported candidate domain")

    values = routing_signal_values(task_frame)
    scores: dict[str, int] = {domain: 1 for domain in specialists}
    for domain in specialists:
        signals = DOMAIN_SIGNALS[domain]
        scores[domain] += sum(
            1
            for value in values
            if value in signals or any(signal in value for signal in signals)
        )
    artifacts = task_frame["scope"]["artifacts"]
    if artifacts:
        anchor_kind = str(artifacts[0]["kind"]).lower()
        for domain in specialists:
            if anchor_kind in DOMAIN_SIGNALS[domain] or any(
                signal in anchor_kind for signal in DOMAIN_SIGNALS[domain]
            ):
                scores[domain] += 2
    if "learn" in task_frame["objective"]["work_types"] and "mentor" in scores:
        scores["mentor"] += 3

    selected = max(specialists, key=lambda domain: (scores[domain], -specialists.index(domain)))
    secondary = [domain for domain in specialists if domain != selected]
    return selected, secondary


def select_mode(task_frame: dict[str, Any], family_class: str) -> str:
    requested = task_frame["execution_preferences"]["requested_mode"]
    if requested:
        return requested
    return "fast" if family_class in {"A", "D", "E"} else "standard"


def select_effort(task_frame: dict[str, Any], family_class: str) -> str:
    requested = task_frame["execution_preferences"]["requested_effort"]
    if requested:
        return requested
    return {"A": "low", "B": "high", "C": "high", "D": "low", "E": "medium"}[family_class]


def governance_blockers(task_frame: dict[str, Any]) -> list[str]:
    governance = task_frame["governance"]
    values: list[str] = []
    for field in ("permissions_required", "confirmations_required"):
        for item in governance[field]:
            if item["status"] == "required":
                values.append(item["id"])
    return unique_strings(values)


def compile_handoff(
    task_frame: dict[str, Any],
    acceptance: dict[str, Any],
    family_class: str,
    selected_domain: str,
    mode: str,
    effort: str,
    references: list[str],
) -> dict[str, Any]:
    scope = task_frame["scope"]
    constraints = task_frame["constraints"]

    focus_in = [item["description"] for item in scope["artifacts"] if item["required"]]
    focus_in.extend(criterion_statements(constraints["hard"]))
    if not focus_in:
        focus_in = ["Deliver only the normalized mission and its acceptance contract."]

    focus_out = criterion_statements(constraints["exclusions"])
    focus_out.extend(criterion_statements(acceptance["forbidden_results"]))
    if not focus_out:
        focus_out = ["Do not expand beyond the bounded mission and acceptance contract."]

    verification_plan = acceptance["verification_plan"]
    evidence = criterion_statements(acceptance["evidence_requirements"]["required_evidence"])
    for field in ("deterministic_checks", "model_checks", "human_review"):
        evidence.extend(check_descriptions(verification_plan[field]))
    if not evidence:
        evidence = ["Return a concise self-check against every acceptance criterion."]

    acceptance_criteria: list[str] = []
    for field in ("required_outcomes", "required_artifacts", "hard_checks"):
        acceptance_criteria.extend(criterion_statements(acceptance[field]))

    timebox = 5 if mode == "fast" else 12
    return {
        "task_id": versioned_ref(task_frame["identity"]["frame_id"], task_frame["identity"]["version"]),
        "assigned_domain": selected_domain,
        "assigned_agent": DOMAIN_AGENTS[selected_domain],
        "class": family_class,
        "mode": mode,
        "effort": effort,
        "mission": task_frame["objective"]["normalized_goal"],
        "focus_in": unique_strings(focus_in),
        "focus_out": unique_strings(focus_out),
        "references": references,
        "evidence": unique_strings(evidence),
        "acceptance_criteria": unique_strings(acceptance_criteria),
        "blocked_by": [],
        "timeout_policy": (
            f"Stop after {timebox} minutes at the packet boundary; preserve artifacts and return "
            "the exact blocker instead of restarting the workflow."
        ),
        "repair_budget": 0 if mode == "fast" else 1,
    }


def compile_core_projection(data: dict[str, Any]) -> dict[str, Any]:
    task_frame = data["task_frame"]
    acceptance = data["acceptance_contract"]
    clarification = data["clarification_decision"]
    family_class = project_family_class(task_frame)
    posture = project_posture(task_frame)
    mode = select_mode(task_frame, family_class)
    effort = select_effort(task_frame, family_class)

    clarification_blocks = clarification["blocks_execution"]
    blockers = unique_strings(
        [*clarification["affected_uncertainty_ids"], *governance_blockers(task_frame)]
    )
    if governance_blockers(task_frame) and not clarification_blocks:
        raise ProjectionError("required permission or confirmation is not blocking execution")

    if clarification_blocks:
        disposition = {"ask": "clarify", "confirm": "confirm", "refuse": "refuse"}[
            clarification["action"]
        ]
        selected_domain = "core"
        secondary_domains: list[str] = []
    elif family_class == "D":
        disposition = "direct"
        selected_domain = "core"
        secondary_domains = []
    else:
        selected_domain, secondary_domains = select_domain(task_frame)
        disposition = "direct" if selected_domain == "core" else "delegate"

    source = task_frame["source"]
    references = unique_strings(
        [
            *source["trusted_context_refs"],
            *(item["ref"] for item in task_frame["scope"]["dependencies"]),
        ]
    )
    hard_checks = criterion_statements(acceptance["hard_checks"])
    dimensions = acceptance["quality_rubric"]["dimensions"]
    verification_plan = acceptance["verification_plan"]
    verification_required = bool(
        hard_checks
        or verification_plan["deterministic_checks"]
        or verification_plan["model_checks"]
        or verification_plan["human_review"]
    )
    stop_conditions = criterion_statements(acceptance["control"]["stop_conditions"])

    clarification_projection = None
    if clarification_blocks:
        clarification_projection = {
            "action": clarification["action"],
            "reasons": clarification["reasons"]
            or ["Execution is blocked by the validated clarification decision."],
            "question": clarification["question"],
            "options": clarification["options"],
            "blocked_by": blockers or ["policy.blocked"],
        }

    handoff = None
    if disposition == "delegate":
        handoff = compile_handoff(
            task_frame,
            acceptance,
            family_class,
            selected_domain,
            mode,
            effort,
            references,
        )

    identity = task_frame["identity"]
    task_ref = versioned_ref(identity["frame_id"], identity["version"])
    projection = {
        "decision_id": f"route.{identity['frame_id']}@{identity['version']}",
        "task_frame_ref": task_ref,
        "acceptance_contract_ref": task_frame["acceptance_contract_ref"],
        "disposition": disposition,
        "family_class": family_class,
        "project_posture": posture,
        "selected_domain": selected_domain,
        "selected_agent": DOMAIN_AGENTS[selected_domain],
        "secondary_domains": secondary_domains,
        "mode": mode,
        "effort": effort,
        "required_references": references,
        "quality_gate": {
            "hard_checks": hard_checks,
            "rubric_dimensions": [item["id"] for item in dimensions],
            "critical_dimensions": acceptance["quality_rubric"]["critical_dimensions"],
        },
        "verification_required": verification_required,
        "stop_conditions": stop_conditions,
        "clarification": clarification_projection,
        "handoff_packet": handoff,
    }
    return projection


def find_banned_keys(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in BANNED_PROJECTION_KEYS:
                found.append(child_path)
            found.extend(find_banned_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_banned_keys(child, f"{path}[{index}]"))
    return found


def projection_summary(projection: dict[str, Any]) -> dict[str, Any]:
    return {
        "disposition": projection["disposition"],
        "family_class": projection["family_class"],
        "project_posture": projection["project_posture"],
        "selected_domain": projection["selected_domain"],
        "selected_agent": projection["selected_agent"],
        "secondary_domains": projection["secondary_domains"],
        "mode": projection["mode"],
        "effort": projection["effort"],
        "handoff_required": projection["handoff_packet"] is not None,
    }


def build_validators(root: pathlib.Path) -> tuple[Draft202012Validator, ...]:
    format_checker = FormatChecker()
    task = Draft202012Validator(
        load_json_schema(root / TASK_FRAME_SCHEMA), format_checker=format_checker
    )
    acceptance = Draft202012Validator(
        load_json_schema(root / ACCEPTANCE_SCHEMA), format_checker=format_checker
    )
    routing = Draft202012Validator(
        load_json_schema(root / ROUTING_SCHEMA), format_checker=format_checker
    )
    return task, acceptance, routing


def routing_schema_errors(
    projection: dict[str, Any], validator: Draft202012Validator
) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            validator.iter_errors(projection),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        )
    ]


def run_fixture_suite(root: pathlib.Path, fixture_dir: pathlib.Path) -> int:
    task_validator, acceptance_validator, routing_validator = build_validators(root)
    paths = sorted([*fixture_dir.rglob("*.yaml"), *fixture_dir.rglob("*.yml")])
    failures = 0
    for path in paths:
        try:
            data = materialize_fixture(path, load_mapping(path))
        except ValueError as exc:
            print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
            failures += 1
            continue

        interpreter_issues = validate_bundle(data, task_validator, acceptance_validator)
        expected_validation = data.get("expected_validation", "pass")
        if expected_validation == "fail":
            if interpreter_issues:
                print(f"PASS {path.as_posix()}: invalid Interpreter fixture was not routed")
            else:
                print(f"FAIL {path.as_posix()}: invalid fixture unexpectedly validated", file=sys.stderr)
                failures += 1
            continue
        if interpreter_issues:
            print(f"FAIL {path.as_posix()}: Interpreter validation failed", file=sys.stderr)
            for issue in interpreter_issues:
                print(f"  {issue.render()}", file=sys.stderr)
            failures += 1
            continue

        expected = data.get("expected_core_projection")
        expected_error = data.get("expected_core_error")
        try:
            projection = compile_core_projection(data)
        except ProjectionError as exc:
            if expected_error == str(exc):
                print(f"PASS {path.as_posix()}: Core refused route: {exc}")
            else:
                print(f"FAIL {path.as_posix()}: {exc}", file=sys.stderr)
                failures += 1
            continue
        if expected_error is not None:
            print(
                f"FAIL {path.as_posix()}: expected Core error {expected_error!r}",
                file=sys.stderr,
            )
            failures += 1
            continue
        schema_errors = routing_schema_errors(projection, routing_validator)
        banned_keys = find_banned_keys(projection)
        actual = projection_summary(projection)
        if expected != actual or schema_errors or banned_keys:
            print(f"FAIL {path.as_posix()}: Core projection mismatch", file=sys.stderr)
            if expected != actual:
                print(f"  expected: {expected}", file=sys.stderr)
                print(f"  actual:   {actual}", file=sys.stderr)
            for error in schema_errors:
                print(f"  schema: {error}", file=sys.stderr)
            if banned_keys:
                print(f"  transcript keys leaked: {', '.join(banned_keys)}", file=sys.stderr)
            failures += 1
        else:
            print(
                f"PASS {path.as_posix()}: disposition={actual['disposition']}, "
                f"domain={actual['selected_domain']}, handoff={actual['handoff_required']}"
            )

    if failures:
        print(f"Core projection fixture validation failed: {failures}/{len(paths)} case(s)")
        return 1
    print(f"Core projection fixture validation passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path, help="validated Interpreter bundle")
    parser.add_argument("--fixtures", action="store_true", help="run all Interpreter fixtures")
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    return parser.parse_args(argv)


def resolve_under(root: pathlib.Path, path: pathlib.Path) -> pathlib.Path:
    return path if path.is_absolute() else root / path


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    if args.fixtures == bool(args.input):
        print("error: choose exactly one of --fixtures or --input", file=sys.stderr)
        return 2
    if args.fixtures:
        return run_fixture_suite(root, root / DEFAULT_FIXTURE_DIR)

    try:
        data = load_mapping(resolve_under(root, args.input))
        task_validator, acceptance_validator, routing_validator = build_validators(root)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    issues = validate_bundle(data, task_validator, acceptance_validator)
    if issues:
        for issue in issues:
            print(f"error: {issue.render()}", file=sys.stderr)
        print(f"Core projection refused invalid Interpreter bundle: {len(issues)} issue(s)")
        return 1
    try:
        projection = compile_core_projection(data)
    except ProjectionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    schema_errors = routing_schema_errors(projection, routing_validator)
    if schema_errors:
        for error in schema_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    banned_keys = find_banned_keys(projection)
    if banned_keys:
        print(f"error: transcript keys leaked: {', '.join(banned_keys)}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(projection, indent=2, ensure_ascii=True))
    else:
        print(yaml.safe_dump(projection, sort_keys=False, allow_unicode=False).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
