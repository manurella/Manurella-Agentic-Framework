"""Record one privacy-bounded guarded parser observation from a live request."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from compile_model_inference import guarded_inference_decision, source_projection
from evaluate_model_inference import inference_from_frame
from parse_task_frame import compile_envelope, error_messages


RESULT_SCHEMA = pathlib.Path("schemas/evals/guarded-live-observation-result.schema.json")
PROMOTION = pathlib.Path("evals/results/stepfun-inference-v1-promotion.parser-promotion.yaml")


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / RESULT_SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def resolve_ref(root: pathlib.Path, path: pathlib.Path) -> tuple[pathlib.Path, str]:
    resolved = path if path.is_absolute() else root / path
    resolved = resolved.resolve()
    try:
        ref = resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"evidence path must be inside the repository: {resolved}") from exc
    return resolved, ref


def fingerprint_request(envelope: dict[str, Any]) -> str:
    request = source_projection(envelope)["authenticated_request"]
    return "sha256:" + hashlib.sha256(request.encode("utf-8")).hexdigest()


def build_record(
    root: pathlib.Path,
    observation_id: str,
    envelope: dict[str, Any],
    locale: str,
    envelope_ref: str,
    inference: dict[str, Any],
    inference_ref: str,
    model: str,
    prompt_version: str,
    promotion: dict[str, Any],
    promotion_ref: str,
    sensitivity_review: str,
    review_status: str,
    reviewer: str | None,
    review_notes: list[str],
) -> dict[str, Any]:
    decision = guarded_inference_decision(
        root,
        envelope,
        locale,
        inference,
        model,
        prompt_version,
        promotion,
        promotion_ref,
    )
    candidate = decision["candidate"]
    record = {
        "schema_version": "guarded-live-observation-result.v0",
        "observation_id": observation_id,
        "evidence_class": "live_request",
        "captured_at": envelope["received_at"],
        "source": {
            "envelope_ref": envelope_ref,
            "inference_ref": inference_ref,
            "request_fingerprint": fingerprint_request(envelope),
            "capture_authorized": True,
            "sensitivity_review": sensitivity_review,
        },
        "candidate": {"model": model, "prompt_version": prompt_version},
        "promotion": decision["promotion"],
        "decision": {
            "disposition": decision["disposition"],
            "selected_parser": decision["selected_parser"],
            "schema_valid": candidate["schema_valid"],
            "trust_aligned": candidate["trust_aligned"],
            "semantic_valid": candidate["semantic_valid"],
            "routing_valid": candidate["routing_valid"],
            "issues": candidate["issues"],
        },
        "human_review": {
            "status": review_status,
            "reviewer": reviewer,
            "notes": review_notes,
        },
        "activation": {
            "status": "pending_human_review" if review_status == "pending" else "evidence_recorded",
            "default_mode": "shadow",
            "reasons": [
                "A live observation records evidence but cannot change the default parser mode.",
                "Default activation criteria require a separately researched and reviewed decision.",
            ],
        },
    }
    issues = error_messages(validator(root), record)
    if issues:
        raise ValueError("invalid guarded live observation: " + "; ".join(issues))
    return record


def run_self_test(root: pathlib.Path) -> None:
    fixture_path = root / "evals/fixtures/task-frame-parser/quick-fix.yaml"
    fixture = load_yaml(fixture_path)
    envelope = fixture["envelope"]
    frame, issues = compile_envelope(root, envelope, fixture.get("locale", "en-US"))
    if frame is None or issues:
        raise ValueError("self-test could not compile deterministic inference")
    promotion = load_yaml(root / PROMOTION)
    record = build_record(
        root,
        "guarded-live-self-test",
        envelope,
        fixture.get("locale", "en-US"),
        "evals/fixtures/task-frame-parser/quick-fix.yaml",
        inference_from_frame(frame),
        "self-test://deterministic-inference",
        promotion["model"],
        promotion["prompt_version"],
        promotion,
        PROMOTION.as_posix(),
        "non_sensitive",
        "pending",
        None,
        [],
    )
    serialized = yaml.safe_dump(record, sort_keys=False)
    raw_request = source_projection(envelope)["authenticated_request"]
    if raw_request in serialized:
        raise ValueError("live observation leaked raw request text")
    if record["decision"]["disposition"] != "candidate_selected":
        raise ValueError("promoted self-test inference was not selected")
    if record["activation"]["default_mode"] != "shadow":
        raise ValueError("single live observation changed the default mode")
    print("guarded live observation self-test passed: selected=1, raw-request=absent, default=shadow")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--observation-id", default="guarded-live-observation")
    parser.add_argument("--input", type=pathlib.Path)
    parser.add_argument("--inference", type=pathlib.Path)
    parser.add_argument("--model", required=False)
    parser.add_argument("--prompt-version", required=False)
    parser.add_argument("--promotion", type=pathlib.Path, default=PROMOTION)
    parser.add_argument("--sensitivity-review", choices=("non_sensitive", "redacted"))
    parser.add_argument("--review-status", choices=("pending", "pass", "fail"), default="pending")
    parser.add_argument("--reviewer")
    parser.add_argument("--review-note", action="append", default=[])
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
        required = (args.input, args.inference, args.model, args.prompt_version, args.sensitivity_review, args.output)
        if any(value is None for value in required):
            raise ValueError(
                "provide --input, --inference, --model, --prompt-version, "
                "--sensitivity-review, and --output"
            )
        envelope_path, envelope_ref = resolve_ref(root, args.input)
        inference_path, inference_ref = resolve_ref(root, args.inference)
        promotion_path, promotion_ref = resolve_ref(root, args.promotion)
        output_path, _ = resolve_ref(root, args.output)
        if (root / "evals/results").resolve() not in output_path.parents:
            raise ValueError("live observation output must be stored under evals/results/")
        if output_path.exists() and not args.overwrite:
            raise ValueError(f"output already exists: {output_path}")
        document = load_yaml(envelope_path)
        envelope = document.get("envelope", document)
        record = build_record(
            root,
            args.observation_id,
            envelope,
            document.get("locale", "en-US"),
            envelope_ref,
            load_yaml(inference_path),
            inference_ref,
            args.model,
            args.prompt_version,
            load_yaml(promotion_path),
            promotion_ref,
            args.sensitivity_review,
            args.review_status,
            args.reviewer,
            args.review_note,
        )
        output_path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8", newline="\n")
        print(f"wrote: {output_path}")
        print(
            f"disposition={record['decision']['disposition']}, "
            f"review={record['human_review']['status']}, default={record['activation']['default_mode']}"
        )
        return 0
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
