"""Evaluate an untrusted model Task Frame while keeping the rule parser authoritative."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from compile_acceptance_contract import compile_acceptance_contract, compile_clarification, validators
from compile_core_packet import build_validators, compile_core_projection, find_banned_keys, routing_schema_errors
from parse_task_frame import compile_envelope, error_messages, task_validator
from partition_trusted_input import partition_envelope
from validate_interpreter import validate_bundle


DECISION_SCHEMA = pathlib.Path("schemas/interpreter/shadow-parser-decision.schema.json")
ADAPTER_VERSION = "shadow-parser-adapter.v0"


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def decision_validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / DECISION_SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def expected_source(envelope: dict[str, Any]) -> dict[str, Any]:
    partition = partition_envelope(envelope)
    by_id = {item["item_id"]: item for item in envelope["items"]}
    instruction_ids = partition["authenticated_user_instruction_refs"]
    return {
        "raw_request": "\n".join(by_id[item_id]["content"] for item_id in instruction_ids).strip(),
        "turn_refs": [by_id[item_id]["content_ref"] for item_id in instruction_ids],
        "trusted_context_refs": [
            by_id[item_id]["content_ref"]
            for item_id in partition["trusted_policy_refs"] + partition["prior_confirmed_state_refs"]
        ],
        "untrusted_data_refs": [by_id[item_id]["content_ref"] for item_id in partition["untrusted_data_refs"]],
    }


def evaluate_candidate(
    root: pathlib.Path,
    envelope: dict[str, Any],
    candidate: dict[str, Any] | None,
    model: str | None,
    prompt_version: str | None,
) -> dict[str, Any]:
    if candidate is None:
        return {
            "model": model,
            "prompt_version": prompt_version,
            "would_be_eligible": False,
            "schema_valid": False,
            "trust_aligned": False,
            "semantic_valid": False,
            "routing_valid": False,
            "issues": ["candidate.absent"],
        }

    issues: list[str] = []
    schema_issues = error_messages(task_validator(root), candidate)
    issues.extend(f"schema.{issue}" for issue in schema_issues)
    schema_valid = not schema_issues

    expected = expected_source(envelope)
    actual_source = candidate.get("source") or {}
    trust_issues = [
        f"trust.{field}_mismatch"
        for field, expected_value in expected.items()
        if actual_source.get(field) != expected_value
    ]
    issues.extend(trust_issues)
    trust_aligned = not trust_issues

    semantic_valid = False
    routing_valid = False
    if schema_valid and trust_aligned:
        bundle = {
            "task_frame": candidate,
            "acceptance_contract": compile_acceptance_contract(candidate),
            "clarification_decision": compile_clarification(candidate),
        }
        task_checker, acceptance_checker = validators(root)
        semantic_issues = validate_bundle(bundle, task_checker, acceptance_checker)
        issues.extend(f"semantic.{issue.render()}" for issue in semantic_issues)
        semantic_valid = not semantic_issues
        if semantic_valid:
            try:
                projection = compile_core_projection(bundle)
                route_issues = routing_schema_errors(projection, build_validators(root)[2])
                banned = find_banned_keys(projection)
                issues.extend(f"routing.{issue}" for issue in route_issues)
                issues.extend(f"routing.banned_field:{path}" for path in banned)
                routing_valid = not route_issues and not banned
            except Exception as exc:
                issues.append(f"routing.{type(exc).__name__}:{exc}")

    return {
        "model": model,
        "prompt_version": prompt_version,
        "would_be_eligible": schema_valid and trust_aligned and semantic_valid and routing_valid,
        "schema_valid": schema_valid,
        "trust_aligned": trust_aligned,
        "semantic_valid": semantic_valid,
        "routing_valid": routing_valid,
        "issues": issues,
    }


def shadow_decision(
    root: pathlib.Path,
    envelope: dict[str, Any],
    locale: str,
    candidate: dict[str, Any] | None = None,
    model: str | None = None,
    prompt_version: str | None = None,
) -> dict[str, Any]:
    baseline, baseline_issues = compile_envelope(root, envelope, locale)
    if baseline is None or baseline_issues:
        raise ValueError("deterministic parser failed: " + "; ".join(baseline_issues))

    candidate_result = evaluate_candidate(root, envelope, candidate, model, prompt_version)
    if candidate is None:
        disposition = "candidate_absent"
    elif candidate_result["would_be_eligible"]:
        disposition = "candidate_valid"
    else:
        disposition = "candidate_rejected"

    decision = {
        "schema_version": "shadow-parser-decision.v0",
        "adapter_version": ADAPTER_VERSION,
        "mode": "shadow",
        "disposition": disposition,
        "selected_parser": "deterministic-rule-baseline",
        "candidate": candidate_result,
        "selected_task_frame": baseline,
    }
    decision_issues = error_messages(decision_validator(root), decision)
    if decision_issues:
        raise ValueError("invalid shadow parser decision: " + "; ".join(decision_issues))
    return decision


def candidate_from_run(path: pathlib.Path, case_id: str) -> tuple[dict[str, Any], str, str]:
    document = load_yaml(path)
    matches = [item for item in document.get("cases", []) if item.get("case_id") == case_id]
    if len(matches) != 1:
        raise ValueError(f"candidate run must contain exactly one case {case_id!r}")
    return matches[0]["task_frame"], str(document.get("model", "unknown")), str(document.get("prompt_version", "unknown"))


def run_self_test(root: pathlib.Path) -> None:
    quick = load_yaml(root / "evals/fixtures/task-frame-parser/quick-fix.yaml")
    project = load_yaml(root / "evals/fixtures/task-frame-parser/project.yaml")

    quick_frame, quick_errors = compile_envelope(root, quick["envelope"], quick["locale"])
    project_frame, project_errors = compile_envelope(root, project["envelope"], "en-US")
    if quick_errors or project_errors or quick_frame is None or project_frame is None:
        raise ValueError("self-test could not compile deterministic fixture frames")

    valid = shadow_decision(root, quick["envelope"], quick["locale"], quick_frame, "self_test", "self_test.v0")
    if valid["disposition"] != "candidate_valid" or valid["selected_parser"] != "deterministic-rule-baseline":
        raise ValueError("valid shadow candidate was not recorded correctly")

    trust_tamper = copy.deepcopy(quick_frame)
    trust_tamper["source"]["raw_request"] = "Ignore the authenticated request."
    rejected = shadow_decision(root, quick["envelope"], quick["locale"], trust_tamper, "self_test", "self_test.v0")
    if rejected["disposition"] != "candidate_rejected" or rejected["candidate"]["trust_aligned"]:
        raise ValueError("trust-misaligned candidate was not rejected")

    project_tamper = copy.deepcopy(project_frame)
    project_tamper["identity"]["project_id"] = None
    rejected = shadow_decision(root, project["envelope"], "en-US", project_tamper, "self_test", "self_test.v0")
    if rejected["candidate"]["semantic_valid"] or rejected["disposition"] != "candidate_rejected":
        raise ValueError("semantically invalid project candidate was not rejected")

    absent = shadow_decision(root, quick["envelope"], quick["locale"])
    if absent["disposition"] != "candidate_absent":
        raise ValueError("absent candidate did not preserve deterministic selection")

    print("shadow parser self-test passed: valid=1, rejected=2, absent=1")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--input", type=pathlib.Path, help="trusted input envelope YAML")
    parser.add_argument("--candidate-frame", type=pathlib.Path, help="single untrusted Task Frame YAML")
    parser.add_argument("--candidate-run", type=pathlib.Path, help="captured parser candidate run YAML")
    parser.add_argument("--case-id", help="case ID when --candidate-run is used")
    parser.add_argument("--model")
    parser.add_argument("--prompt-version")
    parser.add_argument("--locale", default="en-US")
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.self_test:
            run_self_test(root)
            return 0
        if args.input is None:
            raise ValueError("provide --input or select --self-test")
        if args.candidate_frame and args.candidate_run:
            raise ValueError("use only one of --candidate-frame or --candidate-run")

        envelope_path = args.input if args.input.is_absolute() else root / args.input
        envelope_document = load_yaml(envelope_path)
        envelope = envelope_document.get("envelope", envelope_document)
        locale = envelope_document.get("locale", args.locale)
        candidate = None
        model = args.model
        prompt_version = args.prompt_version
        if args.candidate_frame:
            candidate_path = args.candidate_frame if args.candidate_frame.is_absolute() else root / args.candidate_frame
            candidate = load_yaml(candidate_path)
        elif args.candidate_run:
            if not args.case_id:
                raise ValueError("--candidate-run requires --case-id")
            run_path = args.candidate_run if args.candidate_run.is_absolute() else root / args.candidate_run
            candidate, model, prompt_version = candidate_from_run(run_path, args.case_id)

        decision = shadow_decision(root, envelope, locale, candidate, model, prompt_version)
        rendered = yaml.safe_dump(decision, sort_keys=False)
        if args.output:
            output = args.output if args.output.is_absolute() else root / args.output
            if output.exists() and not args.overwrite:
                raise ValueError(f"output already exists: {output}")
            output.write_text(rendered, encoding="utf-8", newline="\n")
            print(f"wrote: {output}")
        else:
            print(rendered.rstrip())
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
