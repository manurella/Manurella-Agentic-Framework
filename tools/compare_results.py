"""Compare two Manurella eval result records."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


SCORE_RE = re.compile(r"^- `([^`]+)`:\s*([1-5](?:\.\d+)?)\s*$")
META_RE = re.compile(r"^- `([^`]+)`:\s*(.*?)\s*$")

DEFAULT_EXCLUDE = {
    "specialist_call_count",
    "repair_loop_count",
    "verifier_count",
}


def parse_fields(path: pathlib.Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = META_RE.match(line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def parse_scores(path: pathlib.Path, include: set[str] | None, exclude: set[str]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = SCORE_RE.match(line.strip())
        if not match:
            continue
        key = match.group(1)
        if include is not None and key not in include:
            continue
        if key in exclude:
            continue
        scores[key] = float(match.group(2))
    return scores


def average(scores: dict[str, float]) -> float:
    if not scores:
        return 0.0
    return sum(scores.values()) / len(scores)


def format_scores(scores: dict[str, float]) -> str:
    if not scores:
        return "  none"
    return "\n".join(f"  {key}: {value:g}" for key, value in sorted(scores.items()))


def parse_csv(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {item.strip() for item in value.split(",") if item.strip()}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=pathlib.Path, required=True)
    parser.add_argument("--guided", type=pathlib.Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--include", help="Comma-separated score keys to include")
    parser.add_argument("--exclude", help="Comma-separated score keys to exclude in addition to defaults")
    args = parser.parse_args(argv)

    include = parse_csv(args.include)
    exclude = set(DEFAULT_EXCLUDE)
    extra_exclude = parse_csv(args.exclude)
    if extra_exclude:
        exclude.update(extra_exclude)

    for path in (args.baseline, args.guided):
        if not path.exists():
            print(f"missing result record: {path}", file=sys.stderr)
            return 1

    baseline_scores = parse_scores(args.baseline, include, exclude)
    guided_scores = parse_scores(args.guided, include, exclude)
    shared = sorted(set(baseline_scores) & set(guided_scores))
    if not shared:
        print("no shared numeric score fields found", file=sys.stderr)
        return 1

    baseline_shared = {key: baseline_scores[key] for key in shared}
    guided_shared = {key: guided_scores[key] for key in shared}
    baseline_avg = average(baseline_shared)
    guided_avg = average(guided_shared)
    delta = guided_avg - baseline_avg
    pass_threshold = delta >= args.threshold

    baseline_meta = parse_fields(args.baseline)
    guided_meta = parse_fields(args.guided)

    print("Manurella result comparison")
    print()
    print(f"baseline: {args.baseline}")
    print(f"  task_id: {baseline_meta.get('task_id', 'unknown')}")
    print(f"  model: {baseline_meta.get('model', 'unknown')}")
    print(f"  mode: {baseline_meta.get('mode', 'unknown')}")
    print(f"guided:   {args.guided}")
    print(f"  task_id: {guided_meta.get('task_id', 'unknown')}")
    print(f"  model: {guided_meta.get('model', 'unknown')}")
    print(f"  mode: {guided_meta.get('mode', 'unknown')}")
    print()
    print("shared scores")
    print(f"baseline average: {baseline_avg:.2f}")
    print(f"guided average:   {guided_avg:.2f}")
    print(f"delta:            {delta:+.2f}")
    print(f"threshold:        +{args.threshold:.2f}")
    print(f"promotion signal: {'pass' if pass_threshold else 'fail'}")
    print()
    print("baseline scores:")
    print(format_scores(baseline_shared))
    print()
    print("guided scores:")
    print(format_scores(guided_shared))
    return 0 if pass_threshold else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
