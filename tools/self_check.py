"""Run Manurella's local framework self-check suite."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys


SMOKE_BASELINE = "self-check-baseline"
SMOKE_GUIDED = "self-check-guided"
SMOKE_MENTOR_OUTPUT = "self-check-mentor-output"
SMOKE_MENTOR_RECORD = "self-check-mentor-record"
SMOKE_LEARNER_STATE = "self-check-learner-state"


def run_command(command: list[str], cwd: pathlib.Path) -> int:
    print(f"> {' '.join(command)}")
    completed = subprocess.run(command, cwd=cwd)
    return completed.returncode


def patch_score(path: pathlib.Path, score: int) -> None:
    text = path.read_text(encoding="utf-8")
    replacements = {
        "- `correctness`:": f"- `correctness`: {score}",
        "- `instruction_adherence`:": f"- `instruction_adherence`: {score}",
        "- `domain_quality`:": f"- `domain_quality`: {score}",
    }
    for before, after in replacements.items():
        text = text.replace(before, after)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_mentor_smoke_output(path: pathlib.Path) -> None:
    text = """# Self Check Mentor Output

## Evidence and assumptions

Evidence used: session protocol, interview study kit, Mentor quality gate.
Assumptions: frontend interview with weak state ownership.

## Target skill

Skill ID: interview.frontend.state-ownership

## Teaching move

Worked example followed by active recall.

## Active recall

Question: Where should filter state, fetched profile data, and form draft state live?

## Answer key or rubric

Expected answer: URL for shareable filters, server cache for fetched profile data, local/form state for drafts.
Scoring rubric: 5 complete, 3 partial, 1 generic.

## Feedback rule

Correct, partially correct, incorrect, or insufficient evidence.

## Learner-state update proposal

Mastery unchanged until unaided recall; next action is another drill.

## Next packet

Next packet: mock interview drill.

## Self-check against Mentor gate

Passed: target skill, active recall, rubric, feedback, learner-state update.
Partial: real learner evidence is synthetic.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def safe_unlink(root: pathlib.Path, path: pathlib.Path) -> None:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    if resolved_root not in resolved_path.parents:
        raise RuntimeError(f"refusing to remove outside repo: {resolved_path}")
    if resolved_path.exists():
        resolved_path.unlink()
        print(f"removed: {resolved_path}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--keep-smoke-records", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    python = sys.executable
    baseline_path = root / "evals" / "results" / f"{SMOKE_BASELINE}.md"
    guided_path = root / "evals" / "results" / f"{SMOKE_GUIDED}.md"
    mentor_output_path = root / "evals" / "results" / f"{SMOKE_MENTOR_OUTPUT}.md"
    mentor_record_path = root / "evals" / "results" / f"{SMOKE_MENTOR_RECORD}.md"
    learner_state_path = root / "evals" / "results" / f"{SMOKE_LEARNER_STATE}.yaml"

    commands = [
        [python, "tools/validate_framework.py", "--repo", "."],
        [python, "tools/partition_trusted_input.py", "--repo", ".", "--fixtures"],
        [python, "tools/parse_task_frame.py", "--repo", ".", "--fixtures"],
        [python, "tools/compile_acceptance_contract.py", "--repo", ".", "--fixtures"],
        [python, "tools/evaluate_task_frame_parser.py", "--repo", ".", "--self-test"],
        [python, "tools/evaluate_parser_promotion.py", "--repo", ".", "--self-test"],
        [python, "tools/shadow_parse_task_frame.py", "--repo", ".", "--self-test"],
        [python, "tools/evaluate_shadow_parser.py", "--repo", ".", "--self-test"],
        [python, "tools/compile_model_inference.py", "--repo", ".", "--self-test"],
        [python, "tools/evaluate_model_inference.py", "--repo", ".", "--self-test"],
        [python, "tools/evaluate_guarded_parser.py", "--repo", ".", "--self-test"],
        [python, "tools/record_guarded_live_observation.py", "--repo", ".", "--self-test"],
        [python, "tools/validate_interpreter.py", "--repo", "."],
        [python, "tools/compile_core_packet.py", "--repo", ".", "--fixtures"],
        [python, "tools/compile_brain_workspace.py", "--repo", ".", "--fixtures"],
        [python, "tools/advance_brain_cycle.py", "--repo", ".", "--fixtures"],
        [python, "tools/compile_runtime_operation.py", "--repo", ".", "--fixtures"],
        [
            python,
            "adapters/kilo/export_agents.py",
            "--all",
            "--output",
            ".kilo/agents",
            "--mode",
            "standard",
            "--effort",
            "high",
            "--dry-run",
        ],
        [
            python,
            "tools/create_result_record.py",
            "--repo",
            ".",
            "--task-id",
            SMOKE_BASELINE,
            "--domain",
            "mentor",
            "--kind",
            "mentor",
            "--benchmark-ref",
            "domains/mentor/benchmarks/README.md#interview-study-benchmarks",
            "--runtime",
            "self_check",
            "--model",
            "self_check",
            "--mode",
            "fast",
            "--effort",
            "medium",
            "--status",
            "partial",
            "--timeout-status",
            "none",
            "--overwrite",
        ],
        [
            python,
            "tools/create_result_record.py",
            "--repo",
            ".",
            "--task-id",
            SMOKE_GUIDED,
            "--domain",
            "mentor",
            "--kind",
            "mentor",
            "--benchmark-ref",
            "domains/mentor/benchmarks/README.md#interview-study-benchmarks",
            "--runtime",
            "self_check",
            "--model",
            "self_check",
            "--mode",
            "standard",
            "--effort",
            "high",
            "--status",
            "partial",
            "--timeout-status",
            "none",
            "--overwrite",
        ],
        [
            python,
            "tools/create_learner_state.py",
            "--repo",
            ".",
            "--learner-id",
            "self-check",
            "--target-role",
            "Frontend Developer",
            "--weak-topics",
            "state ownership, accessibility",
            "--output",
            str(learner_state_path),
            "--overwrite",
        ],
        [
            python,
            "tools/create_mentor_packet.py",
            "--repo",
            ".",
            "--target-role",
            "Frontend Developer",
            "--available-time",
            "30 minutes",
            "--topic",
            "state ownership",
            "--weak-topics",
            "React server and client state",
            "--learner-state",
            str(learner_state_path),
        ],
    ]

    try:
        for command in commands:
            code = run_command(command, root)
            if code != 0:
                return code

        patch_score(baseline_path, 3)
        patch_score(guided_path, 4)
        write_mentor_smoke_output(mentor_output_path)

        code = run_command(
            [
                python,
                "tools/score_mentor_output.py",
                str(mentor_output_path),
                "--min-score",
                "9",
            ],
            root,
        )
        if code != 0:
            return code

        code = run_command(
            [
                python,
                "tools/record_mentor_run.py",
                "--repo",
                ".",
                "--task-id",
                SMOKE_MENTOR_RECORD,
                "--output-text",
                str(mentor_output_path),
                "--runtime",
                "self_check",
                "--model",
                "self_check",
                "--mode",
                "standard",
                "--effort",
                "high",
                "--timeout-status",
                "none",
                "--actual-latency",
                "not_applicable",
                "--overwrite",
            ],
            root,
        )
        if code != 0:
            return code

        code = run_command(
            [
                python,
                "tools/compare_results.py",
                "--baseline",
                str(baseline_path),
                "--guided",
                str(guided_path),
                "--threshold",
                "0.5",
            ],
            root,
        )
        if code != 0:
            return code

        code = run_command(
            [
                python,
                "tools/compare_results.py",
                "--baseline",
                str(baseline_path),
                "--guided",
                str(mentor_record_path),
                "--threshold",
                "0.5",
            ],
            root,
        )
        if code != 0:
            return code
    finally:
        if not args.keep_smoke_records:
            safe_unlink(root, baseline_path)
            safe_unlink(root, guided_path)
            safe_unlink(root, mentor_output_path)
            safe_unlink(root, mentor_record_path)
            safe_unlink(root, learner_state_path)

    print("self-check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
