"""Compile a conservative Task Frame baseline from a trusted input envelope."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from partition_trusted_input import partition_envelope, validators as trust_validators


TASK_FRAME_SCHEMA = pathlib.Path("schemas/interpreter/task-frame.schema.json")
DEFAULT_FIXTURE_DIR = pathlib.Path("evals/fixtures/task-frame-parser")
PARSER_VERSION = "rule-baseline.v0"

PATH_PATTERN = re.compile(r"(?<![\w.-])(?:[A-Za-z]:[\\/])?[\w.-]+(?:[\\/][\w.-]+)*\.(?:md|txt|py|js|ts|tsx|jsx|json|ya?ml|html|css|dart|php|sql)\b", re.I)
VAGUE_PATTERN = re.compile(r"^(?:do|fix|change|update|continue|handle)\s+(?:it|this|that|these|those)\.?$", re.I)

WORK_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("act", re.compile(r"\b(?:send|publish|deploy|delete|remove|purchase|pay|book|post|email)\b", re.I)),
    ("monitor", re.compile(r"\b(?:monitor|watch|track|alert)\b", re.I)),
    ("learn", re.compile(r"\b(?:teach|tutor|learn|study|practice|quiz|interview prep)\b", re.I)),
    ("transform", re.compile(r"\b(?:fix|update|edit|change|refactor|rewrite|repair|modify)\b", re.I)),
    ("analyze", re.compile(r"\b(?:audit|review|analy[sz]e|inspect|investigate|debug|summari[sz]e|research)\b", re.I)),
    ("plan", re.compile(r"\b(?:plan|roadmap|strategy|design)\b", re.I)),
    ("decide", re.compile(r"\b(?:decide|choose|select|recommend|compare)\b", re.I)),
    ("create", re.compile(r"\b(?:create|build|implement|add|write|generate|make|draft)\b", re.I)),
    ("converse", re.compile(r"\b(?:brainstorm|discuss|what do you think|opinion)\b", re.I)),
    ("answer", re.compile(r"^(?:what|why|how|when|where|who|explain|tell me)\b", re.I)),
]

DOMAIN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("core", re.compile(r"\b(?:manurella|agent framework|orchestrat|router|task frame|acceptance contract|eval)\b", re.I)),
    ("mentor", re.compile(r"\b(?:teach|tutor|learn|study|practice|quiz|interview|lesson)\b", re.I)),
    ("pixel", re.compile(r"\b(?:image|illustration|visual|poster|logo|artwork|photo|render)\b", re.I)),
    ("muse", re.compile(r"\b(?:story|novel|scene|character|poem|script|prose|copywriting)\b", re.I)),
    ("build", re.compile(r"\b(?:code|software|repository|repo|file|readme|api|database|schema|test|bug|frontend|backend|deploy)\b", re.I)),
]


def slug(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-.").lower()
    return normalized or "task"


def sentence(value: str) -> str:
    cleaned = " ".join(value.strip().split())
    if not cleaned:
        return "Clarify the requested task."
    return cleaned if cleaned.endswith((".", "?", "!")) else f"{cleaned}."


def infer_work_types(text: str) -> list[str]:
    found = [kind for kind, pattern in WORK_PATTERNS if pattern.search(text)]
    if not found:
        return ["answer"]
    if "converse" in found and set(found) <= {"converse", "answer"}:
        return ["converse"]
    return list(dict.fromkeys(found))


def infer_domains(text: str, work_types: list[str]) -> list[str]:
    domains = [domain for domain, pattern in DOMAIN_PATTERNS if pattern.search(text)]
    if not domains:
        if "learn" in work_types:
            domains.append("mentor")
        elif set(work_types) & {"create", "transform", "act", "monitor"}:
            domains.append("build")
        else:
            domains.append("core")
    return list(dict.fromkeys(domains))


def infer_posture(text: str, work_types: list[str]) -> str | None:
    if re.search(r"\b(?:continue|resume|pick up)\b", text, re.I):
        return "resume"
    if re.search(r"\b(?:audit|review|inspect)\b", text, re.I) and not set(work_types) & {"create", "transform", "act"}:
        return "audit"
    if re.search(r"\b(?:reimagine|redesign|rebuild properly|start over)\b", text, re.I):
        return "reimagine"
    if re.search(r"\b(?:salvage|recover|broken|incomplete)\b", text, re.I):
        return "salvage"
    if "transform" in work_types or re.search(r"\b(?:existing|current|repository|repo|file|readme)\b", text, re.I):
        return "sprint"
    if re.search(r"\b(?:new|from scratch|full project)\b", text, re.I) or "create" in work_types:
        return "genesis"
    return None


def infer_artifacts(text: str, work_types: list[str]) -> list[dict[str, Any]]:
    paths = list(dict.fromkeys(PATH_PATTERN.findall(text)))
    artifacts = []
    for index, path in enumerate(paths, 1):
        suffix = pathlib.PurePath(path.replace("\\", "/")).suffix.lstrip(".").lower() or "file"
        artifacts.append({
            "id": f"artifact.{index}", "kind": suffix,
            "description": f"Referenced artifact {path}.", "required": True,
        })
    if not artifacts and set(work_types) & {"create", "transform"}:
        artifacts.append({
            "id": "artifact.requested-output", "kind": "unspecified",
            "description": "Artifact requested by the authenticated user instruction.", "required": True,
        })
    return artifacts


def infer_constraints(text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    hard: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    clauses = [part.strip() for part in re.split(r"[.;\n]+", text) if part.strip()]
    for clause in clauses:
        if re.search(r"\b(?:do not|don't|must not|without)\b", clause, re.I):
            exclusions.append({
                "id": f"constraint.exclusion-{len(exclusions) + 1}",
                "statement": sentence(clause), "source_authority": "user_asserted",
            })
        elif re.search(r"\b(?:only|must|need(?:s)? to|required)\b", clause, re.I):
            hard.append({
                "id": f"constraint.hard-{len(hard) + 1}",
                "statement": sentence(clause), "source_authority": "user_asserted",
            })
    return hard, exclusions


def parser_findings(text: str, item_refs: list[str]) -> tuple[str, dict[str, list[dict[str, Any]]]]:
    vague = bool(VAGUE_PATTERN.fullmatch(text.strip())) or len(text.split()) < 3
    uncertainty = {"ambiguities": [], "assumptions": [], "missing_information": [], "contradictions": []}
    if vague:
        uncertainty["ambiguities"].append({
            "id": "uncertainty.request-target", "kind": "ambiguity",
            "statement": "The requested target and desired outcome are not explicit.",
            "source_refs": item_refs, "affected_fields": ["objective.normalized_goal", "scope.artifacts"],
            "impact": "material", "status": "open", "resolution": None,
        })
        return "ambiguous", uncertainty
    return "executable", uncertainty


def compile_task_frame(envelope: dict[str, Any], partition: dict[str, Any], locale: str) -> dict[str, Any]:
    by_id = {item["item_id"]: item for item in envelope["items"]}
    instruction_ids = partition["authenticated_user_instruction_refs"]
    raw_request = "\n".join(by_id[item_id]["content"] for item_id in instruction_ids).strip()
    work_types = infer_work_types(raw_request)
    domains = infer_domains(raw_request, work_types)
    clarity, uncertainty = parser_findings(raw_request, instruction_ids)
    frame_slug = slug(envelope["envelope_id"])
    frame_id = f"tf.{frame_slug}"
    hard, exclusions = infer_constraints(raw_request)
    act = "act" in work_types
    destructive = bool(re.search(r"\b(?:delete|remove|destroy|drop|wipe)\b", raw_request, re.I))
    artifacts = infer_artifacts(raw_request, work_types)
    horizon = "project" if re.search(
        r"\b(?:project|continue|resume|entire\s+(?:framework|system)|full\s+(?:project|framework|system))\b",
        raw_request,
        re.I,
    ) else "turn"
    posture = infer_posture(raw_request, work_types)
    if horizon == "project" and posture is None:
        clarity = "ambiguous"
        uncertainty["missing_information"].append({
            "id": "uncertainty.project-posture", "kind": "missing",
            "statement": "The project posture is not explicit.",
            "source_refs": instruction_ids, "affected_fields": ["scope.project_posture"],
            "impact": "material", "status": "open", "resolution": None,
        })
    autonomy = "execute" if set(work_types) & {"create", "transform"} else "advise"
    if re.search(r"\b(?:explain only|do not edit|don't edit|review only|audit only)\b", raw_request, re.I):
        autonomy = "advise"
    if re.search(r"\bdraft\b", raw_request, re.I):
        autonomy = "draft"
    elif re.search(r"\bprepare\b", raw_request, re.I):
        autonomy = "prepare"
    if act:
        autonomy = "execute_with_approval"

    user_content_refs = [by_id[item_id]["content_ref"] for item_id in instruction_ids]
    trusted_refs = [
        by_id[item_id]["content_ref"]
        for item_id in partition["trusted_policy_refs"] + partition["prior_confirmed_state_refs"]
    ]
    untrusted_refs = [by_id[item_id]["content_ref"] for item_id in partition["untrusted_data_refs"]]
    consequence = "critical" if destructive else ("consequential" if act else ("controlled" if set(work_types) & {"create", "transform"} else "minimal"))
    lifecycle = "awaiting_clarification" if clarity == "ambiguous" or consequence in {"consequential", "critical"} else "ready"

    return {
        "identity": {
            "frame_id": frame_id, "version": 1, "parent_frame_id": None,
            "root_frame_id": frame_id,
            "project_id": f"project.{frame_slug}" if horizon == "project" else None,
        },
        "source": {
            "raw_request": raw_request, "turn_refs": user_content_refs,
            "trusted_context_refs": trusted_refs, "untrusted_data_refs": untrusted_refs,
            "timestamp": envelope["received_at"], "locale": locale,
        },
        "objective": {
            "normalized_goal": sentence(raw_request), "work_types": work_types,
            "desired_outcomes": [{
                "id": "outcome.user-request", "statement": sentence(raw_request),
                "kind": "state_change" if act else ("artifact" if artifacts else ("conversation" if "converse" in work_types else "answer")),
                "priority": "required", "source_authority": "user_asserted",
            }],
            "autonomy": autonomy,
        },
        "scope": {
            "horizon": horizon, "clarity": clarity,
            "project_posture": posture,
            "artifacts": artifacts, "dependencies": [],
        },
        "constraints": {
            "hard": hard, "soft": [], "exclusions": exclusions,
            "deadline": None, "freshness": "stable",
        },
        "uncertainty": uncertainty,
        "governance": {
            "consequence": consequence,
            "reversibility": "irreversible" if destructive else "reversible",
            "data_classification": "internal",
            "permissions_required": ([{"id": "permission.requested-action", "capability": "external_action", "status": "required"}] if act else []),
            "confirmations_required": ([{"id": "confirmation.requested-action", "subject": "Execute the requested external or destructive action", "status": "required"}] if act else []),
            "policy_flags": (["destructive_action"] if destructive else []),
        },
        "execution_preferences": {
            "requested_mode": None, "requested_effort": None,
            "latency_preference": None, "cost_preference": None,
        },
        "acceptance_contract_ref": f"ac.{frame_slug}@1",
        "routing_hints": {
            "candidate_domains": domains,
            "required_capabilities": [f"{kind}_task" for kind in work_types],
            "likely_tools": [], "memory_requirements": (["project_state"] if horizon == "project" else []),
            "unresolved_routing_questions": (["Resolve the task target before routing."] if clarity == "ambiguous" else []),
        },
        "provenance": {
            "interpreter_version": PARSER_VERSION, "created_at": envelope["received_at"],
            "entries": [
                {"field_path": "source.raw_request", "authority": "immutable_source", "source_refs": user_content_refs},
                {"field_path": "objective.normalized_goal", "authority": "interpreter_inferred", "source_refs": instruction_ids},
                {"field_path": "governance", "authority": "policy_derived", "source_refs": partition["trusted_policy_refs"] or instruction_ids},
                {"field_path": "routing_hints", "authority": "interpreter_inferred", "source_refs": instruction_ids},
            ],
            "supersedes_frame_ref": None, "changed_fields": [], "invalidated_outputs": [],
        },
        "lifecycle": {"status": lifecycle, "updated_at": envelope["received_at"]},
    }


def task_validator(root: pathlib.Path) -> Draft202012Validator:
    schema = json.loads((root / TASK_FRAME_SCHEMA).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def error_messages(validator: Draft202012Validator, data: Any) -> list[str]:
    errors = sorted(validator.iter_errors(data), key=lambda error: tuple(str(part) for part in error.path))
    return [f"{'.'.join(str(part) for part in error.path) or '$'}: {error.message}" for error in errors]


def get_path(data: Any, path: str) -> Any:
    current = data
    for part in path.split("."):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def compile_envelope(root: pathlib.Path, envelope: dict[str, Any], locale: str) -> tuple[dict[str, Any] | None, list[str]]:
    envelope_validator, _ = trust_validators(root)
    trust_errors = error_messages(envelope_validator, envelope)
    if trust_errors:
        return None, [f"input.{message}" for message in trust_errors]
    partition = partition_envelope(envelope)
    if partition["execution_blocked"]:
        return None, [f"trust.{issue['code']}: {issue['message']}" for issue in partition["issues"] if issue["severity"] == "blocking"]
    frame = compile_task_frame(envelope, partition, locale)
    return frame, [f"task_frame.{message}" for message in error_messages(task_validator(root), frame)]


def run_fixtures(root: pathlib.Path) -> int:
    paths = sorted((root / DEFAULT_FIXTURE_DIR).glob("*.yaml"))
    if not paths:
        print(f"error: no Task Frame parser fixtures under {root / DEFAULT_FIXTURE_DIR}", file=sys.stderr)
        return 1
    failures = 0
    for path in paths:
        fixture = yaml.safe_load(path.read_text(encoding="utf-8"))
        frame, errors = compile_envelope(root, fixture["envelope"], fixture.get("locale", "en-US"))
        expected_error_codes = fixture.get("expected_error_codes", [])
        actual_error_codes = [error.split(":", 1)[0] for error in errors]
        mismatches = []
        if actual_error_codes != expected_error_codes:
            mismatches.append(f"expected errors {expected_error_codes}, got {actual_error_codes}")
        if frame is not None:
            for path_key, expected in fixture.get("expected_fields", {}).items():
                actual = get_path(frame, path_key)
                if actual != expected:
                    mismatches.append(f"{path_key}: expected {expected!r}, got {actual!r}")
            forbidden = fixture.get("forbidden_text", [])
            serialized = json.dumps(frame).lower()
            for value in forbidden:
                if value.lower() in serialized:
                    mismatches.append(f"forbidden text leaked into frame: {value!r}")
        if mismatches:
            failures += 1
            print(f"FAIL {path.as_posix()}", file=sys.stderr)
            for mismatch in mismatches:
                print(f"  {mismatch}", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
        else:
            state = frame["lifecycle"]["status"] if frame else "blocked"
            print(f"PASS {path.as_posix()}: state={state}")
    if failures:
        print(f"Task Frame parser fixtures failed: {failures}/{len(paths)} case(s)")
        return 1
    print(f"Task Frame parser fixtures passed: {len(paths)} case(s)")
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
    frame, errors = compile_envelope(root, envelope, args.locale)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors or frame is None:
        return 1
    print(yaml.safe_dump(frame, sort_keys=False).rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
