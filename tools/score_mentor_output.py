"""Score a Mentor output against the v0 Mentor quality gate."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


CHECKS = [
    {
        "id": "evidence_assumptions",
        "label": "Evidence and assumptions",
        "patterns": [r"\bevidence\b", r"\bassumption"],
        "why": "Mentor must expose what it used and what remains uncertain.",
    },
    {
        "id": "target_skill",
        "label": "Narrow target skill",
        "patterns": [r"\btarget skill\b", r"\bskill id\b", r"interview\.[a-z0-9.-]+"],
        "why": "Mentor must pick one narrow learning target instead of a broad syllabus.",
    },
    {
        "id": "teaching_move",
        "label": "Teaching move",
        "patterns": [r"\bteaching move\b", r"\bdirect instruction\b", r"\bworked example\b", r"\bdrill\b", r"\bmock interview\b"],
        "why": "Mentor must choose how it is teaching, not only explain.",
    },
    {
        "id": "active_recall",
        "label": "Active recall",
        "patterns": [r"\bactive recall\b", r"\bquestion\b", r"\bquiz\b", r"\bexplain-back\b"],
        "why": "Mentor must make the learner retrieve the idea.",
    },
    {
        "id": "rubric_or_answer_key",
        "label": "Answer key or rubric",
        "patterns": [r"\brubric\b", r"\banswer key\b", r"\bexpected answer\b", r"\bscoring\b"],
        "why": "Practice without grading criteria cannot prove learning.",
    },
    {
        "id": "feedback_rule",
        "label": "Feedback rule",
        "patterns": [r"\bfeedback\b", r"\bcorrect\b", r"\bpartially correct\b", r"\bincorrect\b"],
        "why": "Mentor must say how learner answers will be corrected.",
    },
    {
        "id": "learner_state_update",
        "label": "Learner-state update proposal",
        "patterns": [r"\blearner-state\b", r"\blearner state\b", r"\bstate update\b", r"\bmastery\b"],
        "why": "Mentor must propose evidence-bound state changes.",
    },
    {
        "id": "next_packet",
        "label": "Next packet",
        "patterns": [r"\bnext packet\b", r"\bnext action\b", r"\bnext session\b", r"\breview\b"],
        "why": "Mentor must end with a concrete continuation path.",
    },
    {
        "id": "self_check",
        "label": "Self-check against Mentor gate",
        "patterns": [r"\bself-check\b", r"\bmentor gate\b", r"\bpassed\b", r"\bpartial\b"],
        "why": "Mentor must verify itself against the quality gate.",
    },
]


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def status_from_score(score: int, total: int) -> str:
    if score == total:
        return "pass"
    if score >= max(1, total - 2):
        return "partial"
    return "fail"


def score_text(text: str) -> tuple[str, int, list[dict[str, str | bool]]]:
    results: list[dict[str, str | bool]] = []
    for check in CHECKS:
        passed = contains_any(text, list(check["patterns"]))
        results.append(
            {
                "id": str(check["id"]),
                "label": str(check["label"]),
                "passed": passed,
                "why": str(check["why"]),
            }
        )
    score = sum(1 for item in results if item["passed"])
    return status_from_score(score, len(CHECKS)), score, results


def report(path: pathlib.Path, text: str) -> str:
    status, score, results = score_text(text)
    total = len(CHECKS)
    lines = [
        "Mentor output gate score",
        "",
        f"- file: {path}",
        f"- status: {status}",
        f"- score: {score}/{total}",
        "",
        "Checks:",
    ]
    for item in results:
        marker = "pass" if item["passed"] else "missing"
        lines.append(f"- {marker}: {item['label']} ({item['id']})")
        if not item["passed"]:
            lines.append(f"  why: {item['why']}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=pathlib.Path, help="Path to captured Mentor output text or markdown.")
    parser.add_argument("--fail-on-missing", action="store_true", help="Return non-zero unless every check passes.")
    parser.add_argument("--min-score", type=int, default=0, help="Return non-zero if score is below this value.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.output.exists():
        print(f"output does not exist: {args.output}", file=sys.stderr)
        return 1

    text = args.output.read_text(encoding="utf-8")
    status, score, _results = score_text(text)
    print(report(args.output, text))

    if args.fail_on_missing and status != "pass":
        return 1
    if args.min_score and score < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
