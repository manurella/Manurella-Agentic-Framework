"""Create a Mentor learner-state YAML file."""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

import yaml


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "learner"


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def learner_state(args: argparse.Namespace) -> dict[str, object]:
    today = args.date or dt.date.today().isoformat()
    learner_id = slugify(args.learner_id)
    target_role = args.target_role or "unknown"
    weak_topics = split_csv(args.weak_topics)
    required_topics = split_csv(args.required_topics)
    constraints = split_csv(args.constraints)

    skills = []
    next_actions = []
    for topic in weak_topics:
        skill_id = f"interview.custom.{slugify(topic)}"
        skills.append(
            {
                "id": skill_id,
                "label": topic,
                "prerequisites": [],
                "mastery": {
                    "estimate": 0.0,
                    "confidence": "low",
                    "evidence_refs": ["self_report"],
                },
                "recall": {
                    "last_seen": None,
                    "next_review": today,
                    "risk": "unknown",
                },
                "misconceptions": [],
            }
        )
        next_actions.append(
            {
                "type": "diagnose",
                "skill_id": skill_id,
                "reason": "Weak topic provided by learner; diagnostic evidence needed.",
                "urgency": "high",
            }
        )

    if not next_actions:
        next_actions.append(
            {
                "type": "diagnose",
                "skill_id": "interview.core.problem-framing",
                "reason": "Initial diagnostic needed before confident planning.",
                "urgency": "high",
            }
        )

    return {
        "learner_id": learner_id,
        "updated_at": today,
        "goal": {
            "target": target_role,
            "deadline": args.interview_date,
            "context": "interview",
            "constraints": constraints,
        },
        "profile": {
            "domain": "interview",
            "level_estimate": args.level_estimate or "unknown",
            "confidence": "low",
            "notes": [
                "Initial state. Do not infer mastery without evidence.",
            ],
        },
        "skills": skills,
        "recent_events": [
            {
                "id": f"{today}-initial-state",
                "timestamp": today,
                "type": "self_report",
                "skill_ids": [item["id"] for item in skills],
                "summary": "Initial learner state created from user-provided context.",
                "result": "unknown",
                "evidence": "User-provided target role, deadline, weak topics, and constraints.",
            }
        ],
        "next_actions": next_actions,
        "interview": {
            "target_role": target_role,
            "interview_date": args.interview_date,
            "company_or_stack": args.company_or_stack,
            "required_topics": required_topics,
            "weak_topics": weak_topics,
            "mock_history": [],
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--learner-id", required=True)
    parser.add_argument("--target-role")
    parser.add_argument("--interview-date")
    parser.add_argument("--company-or-stack")
    parser.add_argument("--weak-topics")
    parser.add_argument("--required-topics")
    parser.add_argument("--constraints")
    parser.add_argument("--level-estimate")
    parser.add_argument("--date")
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    state = learner_state(args)
    content = yaml.safe_dump(state, sort_keys=False, allow_unicode=False, width=1000)

    if args.output is None:
        print(content)
        return 0

    output = args.output if args.output.is_absolute() else root / args.output
    resolved_output = output.resolve()
    if root not in resolved_output.parents and resolved_output != root:
        print(f"refusing to write outside repo: {resolved_output}", file=sys.stderr)
        return 1
    if output.exists() and not args.overwrite:
        print(f"output already exists: {output}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
