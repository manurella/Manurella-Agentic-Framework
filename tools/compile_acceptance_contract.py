"""Compile and validate an Acceptance Contract for a parsed Task Frame."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from compile_core_packet import (
    build_validators as core_validators,
    compile_core_projection,
    find_banned_keys,
    routing_schema_errors,
)
from parse_task_frame import compile_envelope
from validate_interpreter import (
    ACCEPTANCE_SCHEMA,
    TASK_FRAME_SCHEMA,
    blocking_uncertainty,
    load_json_schema,
    validate_bundle,
)


DEFAULT_FIXTURE_DIR = pathlib.Path("evals/fixtures/acceptance-compiler")
CONSEQUENTIAL_LEVELS = {"consequential", "critical"}


def criterion(identifier: str, statement: str, authority: str = "interpreter_inferred") -> dict[str, str]:
    return {"id": identifier, "statement": statement, "source_authority": authority}


def criterion_authority(authority: str) -> str:
    return authority if authority in {"user_asserted", "interpreter_inferred", "policy_derived"} else "user_asserted"


def contract_identity(task_frame: dict[str, Any]) -> tuple[str, int]:
    ref = task_frame["acceptance_contract_ref"]
    contract_id, raw_version = ref.rsplit("@", 1)
    return contract_id, int(raw_version)


def compile_clarification(task_frame: dict[str, Any]) -> dict[str, Any]:
    blockers = blocking_uncertainty(task_frame)
    governance = task_frame["governance"]
    confirmations = governance["confirmations_required"]
    if blockers:
        statements = "; ".join(item["statement"] for item in blockers)
        return {
            "action": "ask",
            "reasons": ["Open material uncertainty changes the executable task or acceptance criteria."],
            "affected_uncertainty_ids": [item["id"] for item in blockers],
            "question": f"Please clarify: {statements}",
            "options": [],
            "blocks_execution": True,
        }
    if confirmations:
        subjects = "; ".join(item["subject"] for item in confirmations)
        return {
            "action": "confirm",
            "reasons": ["The requested action is consequential or irreversible and requires explicit signoff."],
            "affected_uncertainty_ids": [],
            "question": f"Do you confirm: {subjects}?",
            "options": ["Confirm and proceed", "Do not proceed"],
            "blocks_execution": True,
        }
    return {
        "action": "proceed",
        "reasons": ["The Task Frame is executable without open material uncertainty or required confirmation."],
        "affected_uncertainty_ids": [],
        "question": None,
        "options": [],
        "blocks_execution": False,
    }


def compile_acceptance_contract(task_frame: dict[str, Any]) -> dict[str, Any]:
    contract_id, version = contract_identity(task_frame)
    frame_id = task_frame["identity"]["frame_id"]
    frame_version = task_frame["identity"]["version"]
    objective = task_frame["objective"]
    scope = task_frame["scope"]
    constraints = task_frame["constraints"]
    governance = task_frame["governance"]
    source = task_frame["source"]
    consequence = governance["consequence"]
    signoff = consequence in CONSEQUENTIAL_LEVELS or governance["reversibility"] == "irreversible"

    required_outcomes = [
        criterion(
            f"criterion.outcome-{index}",
            outcome["statement"],
            criterion_authority(outcome["source_authority"]),
        )
        for index, outcome in enumerate(objective["desired_outcomes"], 1)
        if outcome["priority"] == "required"
    ]
    if not required_outcomes:
        required_outcomes.append(
            criterion(
                "criterion.outcome-goal",
                objective["normalized_goal"],
                "interpreter_inferred",
            )
        )
    required_artifacts = [
        criterion(
            f"criterion.artifact-{index}",
            f"Produce {artifact['description']}",
            "interpreter_inferred",
        )
        for index, artifact in enumerate(scope["artifacts"], 1)
        if artifact["required"]
    ]
    hard_checks = [
        criterion(
            f"check.constraint-{index}",
            constraint["statement"],
            criterion_authority(constraint["source_authority"]),
        )
        for index, constraint in enumerate(constraints["hard"], 1)
    ]
    forbidden_results = [
        criterion(
            f"forbidden.exclusion-{index}",
            constraint["statement"],
            criterion_authority(constraint["source_authority"]),
        )
        for index, constraint in enumerate(constraints["exclusions"], 1)
    ]
    forbidden_results.extend(
        criterion(
            f"forbidden.policy-{index}",
            f"Do not bypass policy flag: {flag}.",
            "policy_derived",
        )
        for index, flag in enumerate(governance["policy_flags"], 1)
    )

    threshold = 100 if signoff else 80
    evidence_refs = list(dict.fromkeys(source["turn_refs"] + source["trusted_context_refs"]))
    dimensions = [
        {
            "id": "correctness",
            "description": "Required outcomes and artifacts are factually and functionally correct.",
            "weight": 0.5,
            "minimum_score": threshold,
            "critical": True,
            "evaluator": "core-quality-review",
            "evidence": evidence_refs,
        },
        {
            "id": "instruction_adherence",
            "description": "The result follows authenticated constraints, exclusions, and control boundaries.",
            "weight": 0.5,
            "minimum_score": threshold,
            "critical": True,
            "evaluator": "core-quality-review",
            "evidence": evidence_refs,
        },
    ]

    deterministic_checks = []
    if required_artifacts:
        deterministic_checks.append({
            "id": "deterministic.required-artifacts",
            "description": "Verify every required artifact is present and addressable.",
            "required": True,
        })
    if hard_checks or forbidden_results:
        deterministic_checks.append({
            "id": "deterministic.constraints",
            "description": "Verify hard constraints and forbidden-result conditions against the produced result.",
            "required": True,
        })
    if governance["permissions_required"]:
        deterministic_checks.append({
            "id": "deterministic.permissions",
            "description": "Verify every required permission is granted before action execution.",
            "required": True,
        })

    human_review = []
    if signoff:
        human_review.append({
            "id": "human.signoff",
            "description": "Obtain explicit authenticated signoff before consequential or irreversible execution.",
            "required": True,
        })

    escalation_conditions = []
    if blocking_uncertainty(task_frame):
        escalation_conditions.append(
            criterion("escalate.uncertainty", "Escalate until all open material uncertainty is resolved.", "policy_derived")
        )
    if governance["permissions_required"] or governance["confirmations_required"]:
        escalation_conditions.append(
            criterion("escalate.control", "Escalate if required permission or confirmation is absent or denied.", "policy_derived")
        )

    artifact_kinds = [artifact["kind"] for artifact in scope["artifacts"] if artifact["required"]]
    final_format = ", ".join(artifact_kinds) if artifact_kinds else objective["desired_outcomes"][0]["kind"]
    citations_required = constraints["freshness"] in {"current", "real_time"} or bool(source["untrusted_data_refs"])

    return {
        "contract_id": contract_id,
        "version": version,
        "task_frame_ref": f"{frame_id}@{frame_version}",
        "required_outcomes": required_outcomes,
        "required_artifacts": required_artifacts,
        "hard_checks": hard_checks,
        "forbidden_results": forbidden_results,
        "quality_rubric": {
            "dimensions": dimensions,
            "minimum_score": threshold,
            "critical_dimensions": ["correctness", "instruction_adherence"],
        },
        "evidence_requirements": {
            "freshness": constraints["freshness"],
            "citations_required": citations_required,
            "provenance_required": True,
            "required_evidence": [
                criterion(
                    "evidence.verification",
                    "Record evidence for required checks and quality review before completion.",
                    "policy_derived",
                )
            ],
        },
        "verification_plan": {
            "deterministic_checks": deterministic_checks,
            "model_checks": [{
                "id": "model.quality-review",
                "description": "Evaluate correctness and authenticated instruction adherence against the rubric.",
                "required": True,
            }],
            "human_review": human_review,
        },
        "delivery": {
            "partial_completion_allowed": scope["horizon"] == "project" and not signoff,
            "checkpoint_requirements": [],
            "final_format": final_format,
        },
        "control": {
            "stop_conditions": [
                criterion(
                    "stop.accepted",
                    "Stop when all required outcomes, checks, evidence, and critical rubric thresholds are satisfied.",
                    "policy_derived",
                )
            ],
            "escalation_conditions": escalation_conditions,
            "signoff_required": signoff,
        },
    }


def validators(root: pathlib.Path) -> tuple[Draft202012Validator, Draft202012Validator]:
    checker = FormatChecker()
    return (
        Draft202012Validator(load_json_schema(root / TASK_FRAME_SCHEMA), format_checker=checker),
        Draft202012Validator(load_json_schema(root / ACCEPTANCE_SCHEMA), format_checker=checker),
    )


def compile_bundle(root: pathlib.Path, envelope: dict[str, Any], locale: str = "en-US") -> tuple[dict[str, Any] | None, list[str]]:
    task_frame, parser_errors = compile_envelope(root, envelope, locale)
    if parser_errors or task_frame is None:
        return None, parser_errors
    acceptance = compile_acceptance_contract(task_frame)
    clarification = compile_clarification(task_frame)
    bundle = {
        "task_frame": task_frame,
        "acceptance_contract": acceptance,
        "clarification_decision": clarification,
    }
    task_schema_validator, acceptance_schema_validator = validators(root)
    issues = validate_bundle(bundle, task_schema_validator, acceptance_schema_validator)
    return bundle, [issue.render() for issue in issues]


def get_path(data: Any, path: str) -> Any:
    current = data
    for part in path.split("."):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def load_fixture(path: pathlib.Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    source_ref = data.get("source_fixture")
    if source_ref:
        source = yaml.safe_load((path.parent / source_ref).resolve().read_text(encoding="utf-8"))
        merged = copy.deepcopy(source)
        merged.update({key: value for key, value in data.items() if key != "source_fixture"})
        return merged
    return data


def run_fixtures(root: pathlib.Path) -> int:
    paths = sorted((root / DEFAULT_FIXTURE_DIR).glob("*.yaml"))
    if not paths:
        print(f"error: no Acceptance Contract fixtures under {root / DEFAULT_FIXTURE_DIR}", file=sys.stderr)
        return 1
    failures = 0
    for path in paths:
        fixture = load_fixture(path)
        bundle, errors = compile_bundle(root, fixture["envelope"], fixture.get("locale", "en-US"))
        expected_errors = fixture.get("expected_errors", [])
        mismatches = []
        if errors != expected_errors:
            mismatches.append(f"expected errors {expected_errors}, got {errors}")
        if bundle is not None:
            for field_path, expected in fixture.get("expected_bundle_fields", {}).items():
                actual = get_path(bundle, field_path)
                if actual != expected:
                    mismatches.append(f"{field_path}: expected {expected!r}, got {actual!r}")
            projection = compile_core_projection(bundle)
            routing_validator = core_validators(root)[2]
            for error in routing_schema_errors(projection, routing_validator):
                mismatches.append(f"Core routing schema: {error}")
            for banned_path in find_banned_keys(projection):
                mismatches.append(f"Core routing leaked banned field: {banned_path}")
            for field_path, expected in fixture.get("expected_core_fields", {}).items():
                actual = get_path(projection, field_path)
                if actual != expected:
                    mismatches.append(f"core.{field_path}: expected {expected!r}, got {actual!r}")
        if mismatches:
            failures += 1
            print(f"FAIL {path.as_posix()}", file=sys.stderr)
            for mismatch in mismatches:
                print(f"  {mismatch}", file=sys.stderr)
        else:
            action = bundle["clarification_decision"]["action"] if bundle else "blocked"
            print(f"PASS {path.as_posix()}: decision={action}")
    if failures:
        print(f"Acceptance Contract fixtures failed: {failures}/{len(paths)} case(s)")
        return 1
    print(f"Acceptance Contract fixtures passed: {len(paths)} case(s)")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--locale", default="en-US")
    parser.add_argument("--fixtures", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    if args.fixtures or not args.input:
        return run_fixtures(root)
    path = args.input if args.input.is_absolute() else root / args.input
    envelope = yaml.safe_load(path.read_text(encoding="utf-8"))
    bundle, errors = compile_bundle(root, envelope, args.locale)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors or bundle is None:
        return 1
    print(yaml.safe_dump(bundle, sort_keys=False).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
