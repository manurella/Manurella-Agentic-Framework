"""Create a Manurella eval result record skeleton."""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys


DOMAIN_SCORE_BLOCKS = {
    "frontend": """Frontend evidence when applicable:

- `wcag_target`: WCAG 2.2 AA
- `accessibility_tool`: not_run
- `accessibility_result_path`: not_run
- `lighthouse_result_path`: not_run
- `core_web_vitals`: not_run
- `playwright_result_path`: not_run
- `screenshot_paths`:
- `visual_diff_result`:
- `viewport_coverage`:
- `keyboard_flow_checked`: no
- `screen_reader_semantics_checked`: no
""",
    "mentor": """Mentor evidence when applicable:

- `target_skill`:
- `learner_evidence_used`:
- `diagnosis_confidence`: not_applicable
- `teaching_strategy`:
- `active_recall_included`: no
- `answer_key_or_rubric_included`: no
- `learner_state_update_proposed`: no
- `next_review_or_action`:
""",
}

DOMAIN_SCORE_FIELDS = {
    "frontend": """Frontend scores when applicable:

- `accessibility`:
- `visual_stability`:
- `responsive_fit`:
- `state_correctness`:
- `behavior_correctness`:
- `performance`:
- `implementation_minimality`:
- `verification_evidence`:
""",
    "mentor": """Mentor scores when applicable:

- `diagnostic_precision`:
- `pedagogical_fit`:
- `active_recall_quality`:
- `feedback_quality`:
- `review_schedule_quality`:
- `learner_state_honesty`:
- `interview_readiness_value`:
""",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def read_text(path: pathlib.Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8").strip()


def fenced(text: str) -> str:
    if not text:
        return ""
    return f"\n```text\n{text}\n```\n"


def result_record(args: argparse.Namespace) -> str:
    today = args.date or dt.date.today().isoformat()
    output_text = read_text(args.output_text)
    evidence_text = read_text(args.evidence_text)
    domain_evidence = DOMAIN_SCORE_BLOCKS.get(args.kind, "")
    domain_scores = DOMAIN_SCORE_FIELDS.get(args.kind, "")

    return f"""# {args.task_id}

## Metadata

- `task_id`: {args.task_id}
- `date`: {today}
- `domain`: {args.domain}
- `benchmark_ref`: {args.benchmark_ref}
- `runtime`: {args.runtime}
- `model`: {args.model}
- `mode`: {args.mode}
- `effort`: {args.effort}
- `adapter_version`: {args.adapter_version}
- `prompt_version`: {args.prompt_version}
- `agent_ids`: {args.agent_ids}
- `reviewer`: {args.reviewer}

## Task

Prompt summary:

```text
{args.prompt_summary}
```

Success criteria:

- {args.success_criteria}

Constraints:

- {args.constraints}

## Runtime Outcome

- `status`: {args.status}
- `timeout_status`: {args.timeout_status}
- `target_latency`: {args.target_latency}
- `actual_latency`: {args.actual_latency}
- `specialist_call_count`: {args.specialist_call_count}
- `repair_loop_count`: {args.repair_loop_count}
- `verifier_count`: {args.verifier_count}
- `changed_artifacts`: {args.changed_artifacts}
- `output_path`: {args.output_path}

## Verification

Verification performed:

- {args.verification}

Evidence:
{fenced(evidence_text)}
Verification gaps:

- {args.verification_gaps}

{domain_evidence}
## Scores

Use 1-5 where applicable.

- `correctness`:
- `instruction_adherence`:
- `specificity`:
- `structure`:
- `domain_quality`:
- `safety`:
- `efficiency`:
- `recovery`:

{domain_scores}
## Captured Output
{fenced(output_text)}
## Notes

Quality notes:

- {args.quality_notes}

Failure modes:

- {args.failure_modes}

Next tuning action:

- {args.next_tuning_action}
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--domain", choices=["build", "muse", "pixel", "mentor", "general"], required=True)
    parser.add_argument("--kind", choices=["generic", "frontend", "mentor"], default="generic")
    parser.add_argument("--benchmark-ref", required=True)
    parser.add_argument("--runtime", default="unknown")
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--mode", default="unknown")
    parser.add_argument("--effort", default="unknown")
    parser.add_argument("--adapter-version", default="unknown")
    parser.add_argument("--prompt-version", default="unknown")
    parser.add_argument("--agent-ids", default="unknown")
    parser.add_argument("--reviewer", default="human plus Codex")
    parser.add_argument("--date")
    parser.add_argument("--prompt-summary", default="See captured output or source prompt.")
    parser.add_argument("--success-criteria", default="Not fully recorded.")
    parser.add_argument("--constraints", default="Not fully recorded.")
    parser.add_argument("--status", choices=["pass", "partial", "fail", "timeout"], default="partial")
    parser.add_argument(
        "--timeout-status",
        choices=["none", "upstream_idle_timeout", "user_stopped", "unknown"],
        default="unknown",
    )
    parser.add_argument("--target-latency", default="unknown")
    parser.add_argument("--actual-latency", default="unknown")
    parser.add_argument("--specialist-call-count", default="unknown")
    parser.add_argument("--repair-loop-count", default="unknown")
    parser.add_argument("--verifier-count", default="unknown")
    parser.add_argument("--changed-artifacts", default="unknown")
    parser.add_argument("--output-path", default="not_captured")
    parser.add_argument("--verification", default="Not recorded.")
    parser.add_argument("--verification-gaps", default="Not recorded.")
    parser.add_argument("--quality-notes", default="Not recorded.")
    parser.add_argument("--failure-modes", default="Not recorded.")
    parser.add_argument("--next-tuning-action", default="Review and score this record.")
    parser.add_argument("--output-text", type=pathlib.Path)
    parser.add_argument("--evidence-text", type=pathlib.Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.repo.resolve()
    results_dir = root / "evals" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    task_slug = slugify(args.task_id)
    if not task_slug:
        print("task id must contain at least one alphanumeric character", file=sys.stderr)
        return 1

    output_path = results_dir / f"{task_slug}.md"
    if "fixtures" in output_path.parts:
        print("refusing to write result record inside fixtures", file=sys.stderr)
        return 1
    if output_path.exists() and not args.overwrite:
        print(f"result already exists: {output_path}", file=sys.stderr)
        return 1

    output_path.write_text(result_record(args), encoding="utf-8", newline="\n")
    print(f"wrote: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
