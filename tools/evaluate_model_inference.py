"""Prepare blinded inference packets and evaluate semantic inference candidates."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from compile_model_inference import INFERENCE_SCHEMA, assemble_candidate, create_packet
from evaluate_task_frame_parser import (
    build_result,
    evaluate_baseline,
    evaluate_frame,
    load_corpus,
    load_validator,
    write_result,
)
from parse_task_frame import compile_envelope, error_messages


BLINDED_DIR = pathlib.Path("evals/fixtures/parser-inference-benchmark")
CASE_SCHEMA = pathlib.Path("schemas/evals/parser-inference-benchmark-case.schema.json")
CANDIDATE_SCHEMA = pathlib.Path("schemas/evals/parser-inference-candidate-run.schema.json")
RESULT_SCHEMA = pathlib.Path("schemas/evals/parser-eval-result.schema.json")


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def schema_validator(root: pathlib.Path, schema_path: pathlib.Path) -> Draft202012Validator:
    path = root / schema_path
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    dependency_paths = (
        root / "schemas/interpreter/parser-inference-packet.schema.json",
        root / "schemas/interpreter/task-frame-inference.schema.json",
        root / "schemas/interpreter/task-frame-inference-v1.schema.json",
    )
    registry = Registry()
    for dependency_path in dependency_paths:
        dependency = json.loads(dependency_path.read_text(encoding="utf-8"))
        resource = Resource.from_contents(dependency)
        registry = registry.with_resource(dependency["$id"], resource)
        registry = registry.with_resource(dependency_path.as_uri(), resource)
        registry = registry.with_resource(
            f"https://manurella.dev/schemas/interpreter/{dependency_path.name}", resource
        )
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def prepare_packets(root: pathlib.Path, overwrite: bool) -> list[pathlib.Path]:
    output_dir = root / BLINDED_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    checker = schema_validator(root, CASE_SCHEMA)
    outputs = []
    for case in load_corpus(root):
        document = {
            "schema_version": "parser-inference-benchmark-case.v0",
            "case_id": case["case_id"],
            "packet": create_packet(root, case["envelope"]),
        }
        issues = error_messages(checker, document)
        if issues:
            raise ValueError(f"invalid blinded packet {case['case_id']}: {'; '.join(issues)}")
        name = case["case_id"].split(".")[-1] + ".yaml"
        output = output_dir / name
        if output.exists() and not overwrite:
            raise ValueError(f"blinded packet already exists: {output}")
        output.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8", newline="\n")
        outputs.append(output)
    return outputs


def validate_blinded_packets(root: pathlib.Path) -> None:
    checker = schema_validator(root, CASE_SCHEMA)
    paths = sorted((root / BLINDED_DIR).glob("*.yaml"))
    corpus_ids = {case["case_id"] for case in load_corpus(root)}
    if len(paths) != len(corpus_ids):
        raise ValueError(f"expected {len(corpus_ids)} blinded packets, found {len(paths)}")
    seen = set()
    forbidden_keys = {"expected_fields", "safety_fields", "safety_critical", "envelope", "authentication", "content"}
    for path in paths:
        document = load_yaml(path)
        issues = error_messages(checker, document)
        if issues:
            raise ValueError(f"invalid blinded packet {path}: {'; '.join(issues)}")
        serialized = json.dumps(document, sort_keys=True)
        present = sorted(key for key in forbidden_keys if f'"{key}"' in serialized)
        if present:
            raise ValueError(f"blinded packet {path} leaks forbidden keys: {', '.join(present)}")
        seen.add(document["case_id"])
    if seen != corpus_ids:
        raise ValueError("blinded packet case IDs do not match the private corpus")


def load_candidate(root: pathlib.Path, path: pathlib.Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    resolved = path if path.is_absolute() else root / path
    results_root = (root / "evals/results").resolve()
    if results_root not in resolved.resolve().parents:
        raise ValueError("inference candidate must be stored under evals/results/")
    document = load_yaml(resolved)
    issues = error_messages(schema_validator(root, CANDIDATE_SCHEMA), document)
    if issues:
        raise ValueError("invalid inference candidate run: " + "; ".join(issues))
    cases: dict[str, dict[str, Any]] = {}
    for item in document["cases"]:
        if item["case_id"] in cases:
            raise ValueError(f"duplicate inference case_id: {item['case_id']}")
        cases[item["case_id"]] = item["inference"]
    return document, cases


def evaluate_candidate(
    root: pathlib.Path,
    corpus: list[dict[str, Any]],
    metadata: dict[str, Any],
    inferences: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    corpus_ids = {case["case_id"] for case in corpus}
    unknown = sorted(set(inferences) - corpus_ids)
    if unknown:
        raise ValueError("candidate contains unknown case IDs: " + ", ".join(unknown))
    results = []
    for case in corpus:
        inference = inferences.get(case["case_id"])
        frame = None
        initial = []
        if inference is None:
            initial.append("candidate: missing inference output")
        else:
            try:
                frame = assemble_candidate(root, case["envelope"], case.get("locale", "en-US"), inference)
            except ValueError as exc:
                initial.append(f"inference: {exc}")
        results.append(evaluate_frame(root, case, frame, initial))
    from evaluate_task_frame_parser import summarize

    return {
        "runtime": metadata["runtime"],
        "model": metadata["model"],
        "prompt_version": metadata["prompt_version"],
        "summary": summarize(results, corpus),
        "cases": results,
    }


def inference_from_frame(frame: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "task-frame-inference.v1",
        "normalized_goal": frame["objective"]["normalized_goal"],
        "work_types": frame["objective"]["work_types"],
        "autonomy": frame["objective"]["autonomy"],
        "horizon": frame["scope"]["horizon"],
        "clarity": frame["scope"]["clarity"],
        "project_posture": frame["scope"]["project_posture"],
        "artifacts": [
            {"kind": item["kind"], "description": item["description"], "required": item["required"]}
            for item in frame["scope"]["artifacts"]
        ],
        "hard_constraints": [item["statement"] for item in frame["constraints"]["hard"]],
        "exclusions": [item["statement"] for item in frame["constraints"]["exclusions"]],
        "ambiguities": [
            {"statement": item["statement"], "affected_fields": item["affected_fields"], "impact": item["impact"]}
            for item in frame["uncertainty"]["ambiguities"]
        ],
        "consequence": frame["governance"]["consequence"],
        "reversibility": frame["governance"]["reversibility"],
        "candidate_domains": frame["routing_hints"]["candidate_domains"],
    }


def run_self_test(root: pathlib.Path) -> None:
    validate_blinded_packets(root)
    corpus = load_corpus(root)
    inferences = {}
    for case in corpus:
        frame, issues = compile_envelope(root, case["envelope"], case.get("locale", "en-US"))
        if frame is None or issues:
            raise ValueError(f"self-test baseline compile failed for {case['case_id']}")
        inferences[case["case_id"]] = inference_from_frame(frame)
    metadata = {"runtime": "self_test", "model": "deterministic-inference", "prompt_version": "inference-self-test.v0"}
    result = evaluate_candidate(root, corpus, metadata, inferences)
    if result["summary"]["schema_valid_rate"] != 1 or result["summary"]["semantic_valid_rate"] != 1:
        raise ValueError("self-test inference did not compile to valid Task Frames")
    if result["summary"]["routing_valid_rate"] != 1:
        raise ValueError("self-test inference did not compile through Core routing")
    print("model inference eval self-test passed: blinded=6, schema=1.0, semantic=1.0, routing=1.0")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--run-id", default="model-inference-eval")
    parser.add_argument("--candidate", type=pathlib.Path)
    parser.add_argument("--minimum-accuracy-delta", type=float, default=0.10)
    parser.add_argument("--prepare-packets", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    try:
        if args.prepare_packets:
            outputs = prepare_packets(root, args.overwrite)
            print(f"wrote {len(outputs)} blinded inference packet(s)")
            return 0
        if args.self_test:
            run_self_test(root)
            return 0
        if args.candidate is None:
            raise ValueError("provide --candidate, --prepare-packets, or --self-test")
        validate_blinded_packets(root)
        corpus = load_corpus(root)
        baseline = evaluate_baseline(root, corpus)
        metadata, inferences = load_candidate(root, args.candidate)
        candidate = evaluate_candidate(root, corpus, metadata, inferences)
        result = build_result(args.run_id, baseline, candidate, args.minimum_accuracy_delta)
        issues = error_messages(load_validator(root / RESULT_SCHEMA), result)
        if issues:
            raise ValueError("invalid inference eval result: " + "; ".join(issues))
        output = write_result(root, result, args.overwrite)
        print(f"wrote: {output}")
        print(yaml.safe_dump({"baseline": baseline["summary"], "candidate": candidate["summary"], "promotion": result["promotion"]}, sort_keys=False).rstrip())
        return 0 if result["promotion"]["status"] != "fail" else 2
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
