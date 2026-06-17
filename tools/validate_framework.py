"""Validate Manurella framework structure.

This is a local guardrail for the framework itself. It validates graph links,
agent frontmatter, evidence paths, and eval hygiene before runtime exports or
benchmark runs waste time.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

import yaml


KNOWN_DOMAINS = {"core", "build", "muse", "pixel", "mentor"}
KNOWN_AGENT_TIERS = {"top_level", "internal"}
KNOWN_AGENT_STATUSES = {"draft", "research_candidate", "accepted", "deprecated"}
KNOWN_PERMISSION_VALUES = {"allow", "ask", "deny"}

REQUIRED_AGENT_KEYS = {
    "id",
    "domain",
    "tier",
    "status",
    "purpose",
    "use_when",
    "do_not_use_when",
    "inputs",
    "outputs",
    "permissions",
    "context",
    "workflow",
    "evaluation",
    "failure_modes",
    "research",
}

REQUIRED_NODE_KEYS = {"id", "type", "label", "status", "summary", "owners", "evidence", "updated_at"}
REQUIRED_EDGE_KEYS = {
    "id",
    "type",
    "source",
    "target",
    "status",
    "confidence",
    "weight",
    "evidence",
    "updated_at",
}


class Validator:
    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def rel(self, path: pathlib.Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def existing_path(self, ref: str) -> bool:
        if not ref or ref.startswith(("http://", "https://")):
            return True
        local = ref.split("#", 1)[0]
        if not local:
            return True
        return (self.root / local).exists()

    def looks_like_path(self, ref: str) -> bool:
        if ref.startswith(("http://", "https://")):
            return True
        local = ref.split("#", 1)[0]
        known_prefixes = (
            ".kilo/",
            "adapters/",
            "cognition/",
            "docs/",
            "domains/",
            "evals/",
            "research/",
            "specs/",
            "tools/",
        )
        return (
            local.startswith(known_prefixes)
            or local.startswith(("./", "../"))
            or local.endswith((".md", ".yaml", ".yml", ".json", ".jsonc", ".py", ".txt", ".png"))
        )

    def check_evidence_refs(
        self,
        owner: str,
        refs: Any,
        severity: str = "error",
        require_path_like: bool = True,
    ) -> None:
        if refs is None:
            self.error(f"{owner}: evidence/reference list is missing")
            return
        if not isinstance(refs, list):
            self.error(f"{owner}: evidence/reference field must be a list")
            return
        for ref in refs:
            if not isinstance(ref, str):
                self.error(f"{owner}: evidence/reference must be a string: {ref!r}")
                continue
            if require_path_like and not self.looks_like_path(ref):
                continue
            if not self.existing_path(ref):
                message = f"{owner}: evidence/reference path does not exist: {ref}"
                if severity == "warning":
                    self.warn(message)
                else:
                    self.error(message)

    def parse_frontmatter(self, path: pathlib.Path) -> dict[str, Any] | None:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            self.error(f"{self.rel(path)}: missing YAML frontmatter")
            return None
        parts = text.split("---\n", 2)
        if len(parts) != 3:
            self.error(f"{self.rel(path)}: malformed YAML frontmatter")
            return None
        try:
            data = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError as exc:
            self.error(f"{self.rel(path)}: invalid YAML frontmatter: {exc}")
            return None
        if not isinstance(data, dict):
            self.error(f"{self.rel(path)}: frontmatter must be a mapping")
            return None
        return data

    def validate_graph(self) -> None:
        path = self.root / "cognition" / "graph.yaml"
        if not path.exists():
            self.error("cognition/graph.yaml is missing")
            return
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            self.error(f"cognition/graph.yaml: invalid YAML: {exc}")
            return

        nodes = data.get("nodes")
        edges = data.get("edges")
        if not isinstance(nodes, list):
            self.error("cognition/graph.yaml: nodes must be a list")
            nodes = []
        if not isinstance(edges, list):
            self.error("cognition/graph.yaml: edges must be a list")
            edges = []

        node_ids: set[str] = set()
        for index, node in enumerate(nodes):
            if not isinstance(node, dict):
                self.error(f"cognition/graph.yaml: node[{index}] must be a mapping")
                continue
            node_id = str(node.get("id", ""))
            if not node_id:
                self.error(f"cognition/graph.yaml: node[{index}] missing id")
                continue
            if node_id in node_ids:
                self.error(f"cognition/graph.yaml: duplicate node id: {node_id}")
            node_ids.add(node_id)
            missing = sorted(REQUIRED_NODE_KEYS - set(node))
            if missing:
                self.error(f"graph node {node_id}: missing keys: {', '.join(missing)}")
            self.check_evidence_refs(f"graph node {node_id}", node.get("evidence"))

        edge_ids: set[str] = set()
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                self.error(f"cognition/graph.yaml: edge[{index}] must be a mapping")
                continue
            edge_id = str(edge.get("id", ""))
            if not edge_id:
                self.error(f"cognition/graph.yaml: edge[{index}] missing id")
                continue
            if edge_id in edge_ids:
                self.error(f"cognition/graph.yaml: duplicate edge id: {edge_id}")
            edge_ids.add(edge_id)
            missing = sorted(REQUIRED_EDGE_KEYS - set(edge))
            if missing:
                self.error(f"graph edge {edge_id}: missing keys: {', '.join(missing)}")
            source = edge.get("source")
            target = edge.get("target")
            if source not in node_ids:
                self.error(f"graph edge {edge_id}: unknown source node: {source}")
            if target not in node_ids:
                self.error(f"graph edge {edge_id}: unknown target node: {target}")
            self.check_evidence_refs(f"graph edge {edge_id}", edge.get("evidence"))

    def validate_agents(self) -> None:
        agent_paths = sorted((self.root / "domains").glob("*/agents/*.md"))
        if not agent_paths:
            self.error("no domain agent definitions found")
            return
        seen_ids: set[str] = set()
        for path in agent_paths:
            data = self.parse_frontmatter(path)
            if data is None:
                continue
            agent_id = str(data.get("id", ""))
            owner = f"agent {agent_id or self.rel(path)}"
            if not agent_id:
                self.error(f"{self.rel(path)}: missing agent id")
                continue
            if agent_id in seen_ids:
                self.error(f"{owner}: duplicate agent id")
            seen_ids.add(agent_id)
            if path.stem != agent_id:
                self.error(f"{owner}: filename must match id")

            missing = sorted(REQUIRED_AGENT_KEYS - set(data))
            if missing:
                self.error(f"{owner}: missing required keys: {', '.join(missing)}")

            domain = data.get("domain")
            if domain not in KNOWN_DOMAINS:
                self.error(f"{owner}: unknown domain: {domain}")
            elif path.parts[-3] != domain:
                self.error(f"{owner}: parent domain folder does not match frontmatter domain")

            if data.get("tier") not in KNOWN_AGENT_TIERS:
                self.error(f"{owner}: invalid tier: {data.get('tier')}")
            if data.get("status") not in KNOWN_AGENT_STATUSES:
                self.error(f"{owner}: invalid status: {data.get('status')}")

            permissions = data.get("permissions") or {}
            if not isinstance(permissions, dict):
                self.error(f"{owner}: permissions must be a mapping")
            else:
                for key in ("read", "edit", "shell", "web", "delegate"):
                    value = permissions.get(key)
                    if value not in KNOWN_PERMISSION_VALUES:
                        self.error(f"{owner}: permission {key} must be allow, ask, or deny")

            context = data.get("context") or {}
            if isinstance(context, dict):
                self.check_evidence_refs(
                    owner,
                    context.get("references") or [],
                    severity="warning",
                    require_path_like=True,
                )
            else:
                self.error(f"{owner}: context must be a mapping")

            evaluation = data.get("evaluation") or {}
            if isinstance(evaluation, dict):
                refs = evaluation.get("benchmark_refs") or []
                self.check_evidence_refs(owner, refs, severity="warning", require_path_like=True)
            else:
                self.error(f"{owner}: evaluation must be a mapping")

            research = data.get("research") or {}
            if isinstance(research, dict):
                self.check_evidence_refs(
                    owner,
                    research.get("source_refs") or [],
                    severity="warning",
                    require_path_like=True,
                )
            else:
                self.error(f"{owner}: research must be a mapping")

            if data.get("status") == "accepted":
                benchmark_refs = (evaluation or {}).get("benchmark_refs") or []
                if len(benchmark_refs) < 2:
                    self.error(f"{owner}: accepted agents require at least two benchmark refs")

    def validate_eval_hygiene(self) -> None:
        fixture_eval_files = sorted((self.root / "evals" / "fixtures").glob("**/eval.md"))
        for path in fixture_eval_files:
            self.warn(f"{self.rel(path)}: eval result inside fixture; move durable records to evals/results/")

        result_paths = sorted((self.root / "evals" / "results").glob("*.md"))
        if not result_paths:
            self.warn("evals/results has no result records")
        for path in result_paths:
            text = path.read_text(encoding="utf-8")
            if "`actual_latency`: 0" in text or "- `actual_latency`: 0" in text:
                self.warn(f"{self.rel(path)}: actual_latency is 0; verify this is not placeholder metadata")
            if "model`: unknown" in text:
                self.warn(f"{self.rel(path)}: model is unknown; future evals should capture exact model")

    def run(self) -> int:
        self.validate_graph()
        self.validate_agents()
        self.validate_eval_hygiene()
        for warning in self.warnings:
            print(f"warning: {warning}")
        for error in self.errors:
            print(f"error: {error}", file=sys.stderr)
        if self.errors:
            print(f"validation failed: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
            return 1
        print(f"validation passed: 0 errors, {len(self.warnings)} warning(s)")
        return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path.cwd())
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    return Validator(args.repo.resolve()).run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
