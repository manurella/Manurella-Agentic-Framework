"""Create a copy-paste Mentor interview-study runtime packet."""

from __future__ import annotations

import argparse
import pathlib
import sys


def value_or_unknown(value: str | None) -> str:
    if value is None or not value.strip():
        return "unknown"
    return value.strip()


def packet(args: argparse.Namespace) -> str:
    target_role = value_or_unknown(args.target_role)
    interview_date = value_or_unknown(args.interview_date)
    available_time = value_or_unknown(args.available_time)
    topic = value_or_unknown(args.topic)
    weak_topics = value_or_unknown(args.weak_topics)
    failed_question = value_or_unknown(args.failed_question)
    study_style = value_or_unknown(args.study_style)

    return f"""Use the Manurella Mentor system in {args.mode.title()} Mode with {args.effort.title()} effort.

MANURELLA RUNTIME PACKET
packet_class: verification
mode: {args.mode}
effort: {args.effort}
timebox: {args.timebox} minutes

Framework references:
- domains/mentor/README.md
- domains/mentor/session-protocol.md
- domains/mentor/interview-study-kit.md
- domains/mentor/mentor-quality-gate.md
- domains/mentor/learner-state-schema.md
- specs/runtime-packet-protocol.md
- specs/weak-runtime-compensation.md

Context:
- Target role/interview: {target_role}
- Interview date: {interview_date}
- Available study time: {available_time}
- Target topic: {topic}
- Known weak topics: {weak_topics}
- Recent failed question: {failed_question}
- Preferred study style: {study_style}

Task:
Create one focused interview-study session that improves actual interview readiness.

Before the main answer, output:
1. Evidence read
2. Assumptions
3. Narrow target skill ID or label

Rules:
- Do not create files.
- Use one primary target skill only.
- Do not produce a general syllabus.
- Do not claim mastery from passive reading.
- Do not hide uncertainty.
- Use active recall with answer key or rubric.
- Include feedback rules and a learner-state update proposal.
- Stop after this packet.

Output format:
1. Immediate verdict: usable | partial | blocked
2. Evidence and assumptions
3. Target skill
4. Teaching move
5. Focused concept repair or worked example
6. Active recall set
7. Mock interview drill
8. Answer key or scoring rubric
9. Proposed learner-state update
10. Next packet
11. Self-check against Mentor gate
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--target-role")
    parser.add_argument("--interview-date")
    parser.add_argument("--available-time")
    parser.add_argument("--topic")
    parser.add_argument("--weak-topics")
    parser.add_argument("--failed-question")
    parser.add_argument("--study-style")
    parser.add_argument("--mode", choices=["fast", "standard"], default="standard")
    parser.add_argument(
        "--effort",
        choices=["low", "medium", "high", "extra-high", "max", "ultra"],
        default="high",
    )
    parser.add_argument("--timebox", type=int, default=8)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    content = packet(args)

    if args.output is None:
        print(content)
        return 0

    root = args.repo.resolve()
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
