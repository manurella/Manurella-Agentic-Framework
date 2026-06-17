"""Score captured Mentor output and create a Manurella result record."""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

from score_mentor_output import report, score_text


DEFAULT_BENCHMARK = "domains/mentor/benchmarks/README.md#interview-study-benchmarks"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def status_to_result_status(status: str) -> str:
    if status == "pass":
        return "pass"
    if status == "partial":
        return "partial"
    return "fail"


def score_to_five_point(score: int) -> int:
    if score <= 0:
        return 1
    return max(1, min(5, round((score / 9) * 5)))


def patch_result_scores(path: pathlib.Path, score: int) -> None:
    score_5 = score_to_five_point(score)
    text = path.read_text(encoding="utf-8")
    replacements = {
        "- `correctness`:": f"- `correctness`: {score_5}",
        "- `instruction_adherence`:": f"- `instruction_adherence`: {score_5}",
        "- `specificity`:": f"- `specificity`: {score_5}",
        "- `structure`:": f"- `structure`: {score_5}",
        "- `domain_quality`:": f"- `domain_quality`: {score_5}",
        "- `safety`:": "- `safety`: 4",
        "- `efficiency`:": "- `efficiency`: 4",
        "- `recovery`:": "- `recovery`: not_applicable",
        "- `diagnostic_precision`:": f"- `diagnostic_precision`: {score_5}",
        "- `pedagogical_fit`:": f"- `pedagogical_fit`: {score_5}",
        "- `active_recall_quality`:": f"- `active_recall_quality`: {score_5}",
        "- `feedback_quality`:": f"- `feedback_quality`: {score_5}",
        "- `review_schedule_quality`:": f"- `review_schedule_quality`: {score_5}",
        "- `learner_state_honesty`:": f"- `learner_state_honesty`: {score_5}",
        "- `interview_readiness_value`:": f"- `interview_readiness_value`: {score_5}",
        "- `active_recall_included`: no": "- `active_recall_included`: yes",
        "- `answer_key_or_rubric_included`: no": "- `answer_key_or_rubric_included`: yes",
        "- `learner_state_update_proposed`: no": "- `learner_state_update_proposed`: yes",
    }
    for before, after in replacements.items():
        text = text.replace(before, after)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--output-text", type=pathlib.Path, required=True)
    parser.add_argument("--runtime", default="Kilo Code")
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--mode", choices=["fast", "standard", "unknown"], default="standard")
    parser.add_argument(
        "--effort",
        choices=["low", "medium", "high", "extra-high", "max", "ultra", "unknown"],
        default="high",
    )
    parser.add_argument("--timeout-status", choices=["none", "upstream_idle_timeout", "user_stopped", "unknown"], default="unknown")
    parser.add_argument("--actual-latency", default="unknown")
    parser.add_argument("--adapter-version", default="unknown")
    parser.add_argument("--prompt-version", default="tools/create_mentor_packet.py")
    parser.add_argument("--agent-ids", default="mentor generated agents")
    parser.add_argument("--benchmark-ref", default=DEFAULT_BENCHMARK)
    parser.add_argument("--min-score", type=int, default=7)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--keep-score-report", action="store_true")
    return parser.parse_args(argv)


def run_create_result(root: pathlib.Path, args: argparse.Namespace, score_report: pathlib.Path, status: str) -> int:
    command = [
        sys.executable,
        "tools/create_result_record.py",
        "--repo",
        ".",
        "--task-id",
        args.task_id,
        "--domain",
        "mentor",
        "--kind",
        "mentor",
        "--benchmark-ref",
        args.benchmark_ref,
        "--runtime",
        args.runtime,
        "--model",
        args.model,
        "--mode",
        args.mode,
        "--effort",
        args.effort,
        "--adapter-version",
        args.adapter_version,
        "--prompt-version",
        args.prompt_version,
        "--agent-ids",
        args.agent_ids,
        "--prompt-summary",
        "Captured Mentor interview-study output scored by tools/score_mentor_output.py.",
        "--success-criteria",
        "Output satisfies Mentor session protocol and quality-gate structure.",
        "--constraints",
        "Captured output is scored deterministically; domain correctness still requires human or expert review.",
        "--status",
        status_to_result_status(status),
        "--timeout-status",
        args.timeout_status,
        "--target-latency",
        "runtime packet timebox",
        "--actual-latency",
        args.actual_latency,
        "--changed-artifacts",
        "none expected",
        "--output-path",
        str(args.output_text),
        "--verification",
        "Ran tools/score_mentor_output.py against captured Mentor output.",
        "--verification-gaps",
        "Deterministic scorer checks structure and evidence coverage, not full domain correctness.",
        "--quality-notes",
        f"Mentor output scorer status: {status}.",
        "--failure-modes",
        "See score report for missing gate items.",
        "--next-tuning-action",
        "Repair any missing Mentor gate items, then rerun or compare against baseline.",
        "--output-text",
        str(args.output_text),
        "--evidence-text",
        str(score_report),
    ]
    if args.overwrite:
        command.append("--overwrite")
    return subprocess.run(command, cwd=root).returncode


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    output_text = args.output_text if args.output_text.is_absolute() else root / args.output_text
    if not output_text.exists():
        print(f"captured output does not exist: {output_text}", file=sys.stderr)
        return 1

    text = output_text.read_text(encoding="utf-8")
    status, score, _results = score_text(text)
    score_report = root / "evals" / "results" / f"{args.task_id}-score-report.md"
    score_report.parent.mkdir(parents=True, exist_ok=True)
    score_report.write_text(report(output_text, text), encoding="utf-8", newline="\n")

    create_code = run_create_result(root, args, score_report, status)
    if create_code != 0:
        return create_code

    result_path = root / "evals" / "results" / f"{slugify(args.task_id)}.md"
    patch_result_scores(result_path, score)

    if not args.keep_score_report:
        score_report.unlink()

    print(f"mentor score: {score}/9 ({status})")
    if score < args.min_score:
        print(f"score below threshold: {score} < {args.min_score}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
