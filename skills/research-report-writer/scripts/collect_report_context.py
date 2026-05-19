#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


IGNORE_DIRS = {
    ".git",
    ".codex_tmp",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
}

SOURCE_EXTS = {
    ".md",
    ".tex",
    ".txt",
    ".docx",
    ".pdf",
    ".csv",
    ".tsv",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".log",
    ".bib",
    ".py",
    ".ipynb",
    ".pptx",
}

REPORT_KEYWORDS = (
    "report",
    "paper",
    "summary",
    "analysis",
    "latex",
    "doc",
    "experiment",
    "result",
    "metric",
    "metrics",
    "benchmark",
    "evaluation",
    "ablation",
    "figure",
    "table",
    "reference",
    "references",
    "bibliography",
    "citation",
    "bib",
    "ledger",
    "报告",
    "论文",
    "初稿",
    "每日",
)

SESSION_KEYWORDS = (
    "report",
    "paper",
    "latex",
    "tex",
    "pdf",
    "word",
    "draft",
    "manuscript",
    "experiment",
    "verification",
    "contribution",
    "limitation",
    "报告",
    "论文",
    "初稿",
    "实验",
    "验证",
    "贡献",
    "创新",
    "修正",
    "修订",
    "真实",
)


@dataclass
class Candidate:
    path: Path
    mtime: float
    size: int
    score: int
    kind: str


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if "skills/research-report-writer" in path.as_posix().replace("\\", "/"):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in SOURCE_EXTS:
            continue
        yield path


def classify(path: Path) -> str:
    text = path.as_posix().lower()
    if "/output/latex/" in text:
        return "latex-output"
    if "/output/doc/" in text:
        return "doc-output"
    if "/reports/" in text:
        return "report"
    if "/artifacts/" in text:
        return "artifact"
    if path.suffix.lower() == ".bib":
        return "bibliography"
    if "/scripts/" in text:
        return "script"
    if any(token in text for token in ("/logs/", "/runlogs/", "/tensorboard/", "/wandb/")):
        return "log"
    if "/docs/" in text:
        return "design-doc"
    return "other"


def score_path(path: Path, query_tokens: list[str]) -> int:
    raw = path.as_posix().lower()
    name = path.name.lower()
    score = 0
    score += sum(2 for kw in REPORT_KEYWORDS if kw.lower() in raw)
    if path.suffix.lower() in {".tex", ".docx", ".pdf"}:
        score += 4
    if path.suffix.lower() in {".md", ".txt", ".log", ".jsonl", ".bib"}:
        score += 2
    if "/output/" in raw:
        score += 4
    if "/reports/" in raw:
        score += 3
    if "/artifacts/" in raw:
        score += 2
    if "/scripts/" in raw and ("report" in name or "paper" in name):
        score += 4
    if path.suffix.lower() == ".log" and not any(token in raw for token in ("/logs/", "/runlogs/")):
        score -= 4
    if any(flag in raw for flag in ("superseded", "~$", ".aux", ".out", ".synctex")):
        score -= 8
    if query_tokens:
        score += sum(8 for token in query_tokens if token in raw)
    return score


def read_snippet(path: Path, max_chars: int) -> str:
    if path.suffix.lower() not in {".md", ".tex", ".txt", ".csv", ".tsv", ".json", ".jsonl", ".yaml", ".yml", ".log", ".bib", ".py"}:
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    text = " ".join(text.split())
    return text[:max_chars]


def collect_text(value) -> str:
    parts: list[str] = []

    def walk(item) -> None:
        if item is None:
            return
        if isinstance(item, str):
            parts.append(item)
            return
        if isinstance(item, list):
            for child in item:
                walk(child)
            return
        if isinstance(item, dict):
            if item.get("type") in {"input_text", "output_text", "text"} and isinstance(item.get("text"), str):
                parts.append(item["text"])
                return
            for key in ("text", "content", "message", "arguments"):
                if key in item:
                    walk(item[key])

    walk(value)
    return "\n".join(parts)


def read_session_snippet(path: Path, max_chars: int) -> str:
    if max_chars <= 0:
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    if path.suffix.lower() != ".jsonl":
        compact = " ".join(text.split())
        return compact[:max_chars]

    snippets: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = obj.get("payload", {})
        if payload.get("type") != "message":
            continue
        role = payload.get("role", "")
        if role not in {"user", "assistant"}:
            continue
        body = " ".join(collect_text(payload.get("content", "")).split())
        if not body:
            continue
        if body.startswith("# AGENTS.md instructions") or "<skills_instructions>" in body:
            continue
        lowered = body.lower()
        if any(keyword.lower() in lowered for keyword in SESSION_KEYWORDS):
            snippets.append(f"{role}: {body[:700]}")
        if sum(len(item) for item in snippets) >= max_chars:
            break
    return " ".join(snippets)[:max_chars]


def iter_session_memory_files(codex_home: Path, session_id: str):
    search_roots = [
        codex_home / "sessions",
        codex_home / "archived_sessions",
        codex_home / "memories" / "rollout_summaries",
    ]
    for root in search_roots:
        if not root.exists():
            continue
        pattern = "*.jsonl" if root.name != "rollout_summaries" else "*.md"
        for path in root.rglob(pattern):
            if session_id in path.name:
                yield path
                continue
            try:
                if session_id in path.read_text(encoding="utf-8", errors="ignore"):
                    yield path
            except OSError:
                continue

    for path in [
        codex_home / "memories" / "raw_memories.md",
        codex_home / "memories" / "MEMORY.md",
        codex_home / "memories" / "memory_summary.md",
        codex_home / "session_index.jsonl",
    ]:
        if not path.exists():
            continue
        try:
            if session_id in path.read_text(encoding="utf-8", errors="ignore"):
                yield path
        except OSError:
            continue


def print_session_memory(session_id: str, codex_home: Path, snippet_chars: int) -> None:
    seen: set[Path] = set()
    rows: list[Path] = []
    for path in iter_session_memory_files(codex_home, session_id):
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        rows.append(resolved)

    rows.sort(key=lambda p: (0 if "rollout_summaries" in p.as_posix() else 1, p.as_posix()))
    print("## session-memory\n")
    print(f"- session_id: `{session_id}`")
    print(f"- codex_home: `{codex_home}`")
    print(f"- matches: {len(rows)}\n")
    for path in rows:
        try:
            stat = path.stat()
            stamp = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            size = stat.st_size
        except OSError:
            stamp = "unknown"
            size = 0
        print(f"- `{path}` | modified={stamp} | size={size}")
        snippet = read_session_snippet(path, snippet_chars)
        if snippet:
            print(f"  - snippet: {snippet}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect likely report-writing context files.")
    parser.add_argument("--root", default=".", help="Project root to scan.")
    parser.add_argument("--query", nargs="*", default=[], help="Optional topic/date/stage/satellite query.")
    parser.add_argument("--limit", type=int, default=30, help="Maximum rows per section.")
    parser.add_argument("--snippets", type=int, default=0, help="Snippet chars for text files.")
    parser.add_argument("--session-id", default="", help="Optional Codex session/thread ID to collect memory for.")
    parser.add_argument(
        "--codex-home",
        default=str(Path.home() / ".codex"),
        help="Codex home directory used with --session-id.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    codex_home = Path(args.codex_home).resolve()
    query_text = " ".join(args.query).strip()
    query_tokens = [tok.lower() for tok in query_text.split() if tok.strip()]
    candidates: list[Candidate] = []

    for path in iter_files(root):
        try:
            stat = path.stat()
        except OSError:
            continue
        raw = path.as_posix().lower()
        if query_tokens and not all(token in raw for token in query_tokens):
            continue
        score = score_path(path, query_tokens)
        if score <= 0 and query_tokens:
            continue
        if score <= 1 and not query_tokens:
            continue
        candidates.append(
            Candidate(
                path=path,
                mtime=stat.st_mtime,
                size=stat.st_size,
                score=score,
                kind=classify(path),
            )
        )

    candidates.sort(key=lambda item: (item.score, item.mtime), reverse=True)

    print(f"# Report Context Candidates\n")
    print(f"- root: `{root}`")
    print(f"- query: `{query_text or '(none)'}`")
    print(f"- candidates: {len(candidates)}\n")

    if args.session_id:
        print_session_memory(args.session_id, codex_home, args.snippets or 1600)

    recent = sorted(candidates, key=lambda item: item.mtime, reverse=True)[: args.limit]
    if recent:
        print("## recent-high-signal\n")
        for item in recent:
            rel = item.path.relative_to(root)
            stamp = datetime.fromtimestamp(item.mtime).strftime("%Y-%m-%d %H:%M")
            print(f"- `{rel}` | kind={item.kind} | score={item.score} | modified={stamp} | size={item.size}")
            snippet = read_snippet(item.path, args.snippets)
            if snippet:
                print(f"  - snippet: {snippet}")
        print()

    by_kind: dict[str, list[Candidate]] = {}
    for item in candidates:
        by_kind.setdefault(item.kind, []).append(item)

    for kind in ("doc-output", "latex-output", "report", "artifact", "bibliography", "log", "script", "design-doc", "other"):
        rows = by_kind.get(kind, [])[: args.limit]
        if not rows:
            continue
        print(f"## {kind}\n")
        for item in rows:
            rel = item.path.relative_to(root)
            stamp = datetime.fromtimestamp(item.mtime).strftime("%Y-%m-%d %H:%M")
            print(f"- `{rel}` | score={item.score} | modified={stamp} | size={item.size}")
            snippet = read_snippet(item.path, args.snippets)
            if snippet:
                print(f"  - snippet: {snippet}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
