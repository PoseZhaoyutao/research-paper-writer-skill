#!/usr/bin/env python3
"""Audit a research-paper evidence manifest for missing proof links.

This script is intentionally conservative. It does not prove that a claim is
scientifically true, but it catches common manuscript risks before review:
missing required fields, missing local artifacts, unresolved verification
statuses, and citation keys absent from a supplied BibTeX file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


OK_STATUSES = {"verified", "checked", "complete", "ok", "pass", "passed"}
BAD_VALUES = {
    "",
    "todo",
    "tbd",
    "pending",
    "unknown",
    "missing",
    "unverified",
    "not verified",
    "none found",
}
NONE_VALUES = {"none", "n/a", "na", "not applicable"}
LOCAL_EXTENSIONS = {
    ".bib",
    ".csv",
    ".docx",
    ".h5",
    ".hdf5",
    ".ipynb",
    ".jpg",
    ".jpeg",
    ".json",
    ".jsonl",
    ".log",
    ".mat",
    ".md",
    ".npy",
    ".npz",
    ".pdf",
    ".png",
    ".py",
    ".svg",
    ".tex",
    ".tsv",
    ".txt",
    ".xlsx",
    ".yaml",
    ".yml",
}


SECTION_SPECS = {
    "Manuscript": {
        "start": None,
        "required": ["manuscript path", "manuscript version", "target venue", "venue brief"],
        "path_fields": ["manuscript path", "venue brief"],
        "status_fields": [],
    },
    "Runs": {
        "start": "result id",
        "required": [
            "result id",
            "command",
            "data version",
            "code revision",
            "config",
            "seed",
            "environment",
            "output artifacts",
        ],
        "path_fields": ["config", "output artifacts"],
        "status_fields": [],
    },
    "Figures": {
        "start": "figure id",
        "required": [
            "figure id",
            "raw data",
            "generation script/command",
            "output file",
            "sample set",
            "key claim",
            "verification status",
        ],
        "path_fields": ["raw data", "generation script/command", "output file"],
        "status_fields": ["verification status"],
    },
    "Tables": {
        "start": "table id",
        "required": [
            "table id",
            "raw data",
            "calculation script/command",
            "output file",
            "reported metrics",
            "key claim",
            "verification status",
        ],
        "path_fields": ["raw data", "calculation script/command", "output file"],
        "status_fields": ["verification status"],
    },
    "Formulas": {
        "start": "equation id",
        "required": [
            "equation id",
            "exact implementation or external source",
            "linked run/config",
            "symbol definitions",
            "verification status",
        ],
        "path_fields": ["exact implementation or external source", "linked run/config"],
        "status_fields": ["verification status"],
    },
    "Claims": {
        "start": "claim id",
        "required": [
            "claim id",
            "manuscript location",
            "supporting figures/tables/artifacts/logs",
            "evidence strength",
            "verification status",
        ],
        "path_fields": ["supporting figures/tables/artifacts/logs"],
        "status_fields": ["verification status"],
    },
    "References": {
        "start": "citation key",
        "required": [
            "citation key",
            "verified bibliographic source",
            "sentence or claim supported",
            "source support note",
            "verification status",
        ],
        "path_fields": [],
        "status_fields": ["verification status"],
    },
    "Open Gaps": {
        "start": None,
        "required": [],
        "path_fields": [],
        "status_fields": [],
    },
}


@dataclass
class Finding:
    severity: str
    section: str
    record: str
    field: str
    message: str


def normalize_key(key: str) -> str:
    return re.sub(r"\s+", " ", key.strip().lower())


def is_bad_value(value: str, allow_na: bool = False) -> bool:
    text = normalize_key(value)
    if allow_na and text in NONE_VALUES:
        return False
    return text in BAD_VALUES


def is_external_reference(value: str) -> bool:
    text = value.strip().lower()
    return (
        text.startswith(("http://", "https://", "doi:", "arxiv:", "pmid:", "isbn:"))
        or "doi.org/" in text
        or text.startswith("external:")
    )


def parse_manifest(path: Path) -> dict[str, list[dict[str, str]]]:
    current_section = None
    sections: dict[str, list[dict[str, str]]] = {}
    current_record: dict[str, str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if current_section and current_record is not None:
                sections.setdefault(current_section, []).append(current_record)
            current_section = line[3:].strip()
            current_record = {}
            sections.setdefault(current_section, [])
            continue
        if not current_section or not line.startswith("- ") or ":" not in line:
            continue

        key, value = line[2:].split(":", 1)
        key = normalize_key(key)
        value = value.strip()
        spec = SECTION_SPECS.get(current_section, {})
        start_key = spec.get("start")

        if start_key and key == start_key and current_record:
            sections.setdefault(current_section, []).append(current_record)
            current_record = {}
        if current_record is None:
            current_record = {}
        current_record[key] = value

    if current_section and current_record is not None:
        sections.setdefault(current_section, []).append(current_record)

    return sections


def record_label(section: str, record: dict[str, str], index: int) -> str:
    start = SECTION_SPECS.get(section, {}).get("start")
    if start and record.get(start):
        return record[start]
    return f"{section}#{index + 1}"


def split_reference_tokens(value: str) -> list[str]:
    raw_tokens = re.split(r"[,;]\s*|\band\b|\n", value)
    tokens: list[str] = []
    for token in raw_tokens:
        token = token.strip().strip("`'\"")
        if token:
            tokens.append(token)
    return tokens


def extract_local_path_tokens(value: str) -> list[str]:
    tokens = split_reference_tokens(value)
    found: list[str] = []
    for token in tokens:
        if is_external_reference(token) or normalize_key(token) in NONE_VALUES:
            continue
        command_paths = re.findall(r"[\w./\\:-]+\.(?:py|csv|tsv|json|jsonl|log|png|jpg|jpeg|svg|pdf|tex|bib|xlsx|yaml|yml|txt|md)", token)
        if command_paths:
            found.extend(command_paths)
            continue
        suffix = Path(token).suffix.lower()
        if suffix in LOCAL_EXTENSIONS or "/" in token or "\\" in token:
            found.append(token)
    return found


def path_exists(root: Path, token: str) -> bool:
    cleaned = token.strip().strip("`'\"")
    if not cleaned:
        return True
    p = Path(cleaned)
    if not p.is_absolute():
        p = root / p
    return p.exists()


def read_bib_keys(path: Path | None) -> set[str]:
    if not path:
        return set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", text))


def collect_known_ids(sections: dict[str, list[dict[str, str]]]) -> set[str]:
    ids = set()
    for section, spec in SECTION_SPECS.items():
        start = spec.get("start")
        if not start:
            continue
        for record in sections.get(section, []):
            value = record.get(start)
            if value:
                ids.add(value.strip())
    return ids


def check_manifest(manifest: Path, root: Path, bib: Path | None = None) -> list[Finding]:
    sections = parse_manifest(manifest)
    findings: list[Finding] = []
    known_ids = collect_known_ids(sections)
    bib_keys = read_bib_keys(bib)

    for section, spec in SECTION_SPECS.items():
        records = sections.get(section, [])
        if section != "Open Gaps" and not records:
            findings.append(Finding("error", section, section, "", "Missing section or records"))
            continue

        for index, record in enumerate(records):
            label = record_label(section, record, index)
            for field in spec.get("required", []):
                value = record.get(field, "")
                allow_na = field in {"checkpoint/model version", "seed"}
                if is_bad_value(value, allow_na=allow_na):
                    findings.append(Finding("error", section, label, field, "Missing or unresolved required field"))

            for field in spec.get("status_fields", []):
                value = normalize_key(record.get(field, ""))
                if value not in OK_STATUSES:
                    findings.append(Finding("error", section, label, field, f"Status is not verified: {record.get(field, '')!r}"))

            for field in spec.get("path_fields", []):
                value = record.get(field, "")
                if is_bad_value(value, allow_na=True):
                    findings.append(Finding("error", section, label, field, "Missing traceable file or external source"))
                    continue
                if is_external_reference(value):
                    continue
                tokens = extract_local_path_tokens(value)
                if not tokens and field != "linked run/config":
                    findings.append(Finding("warning", section, label, field, "No local path-like token found"))
                    continue
                for token in tokens:
                    if token in known_ids:
                        continue
                    if not path_exists(root, token):
                        findings.append(Finding("error", section, label, field, f"Referenced file does not exist: {token}"))

            if section == "References":
                source = record.get("verified bibliographic source", "")
                if not is_external_reference(source) and not Path(source).suffix.lower() in {".bib", ".ris"}:
                    findings.append(Finding("warning", section, label, "verified bibliographic source", "Source is not a DOI/URL/arXiv/PMID/ISBN/local bibliography marker"))
                citation_key = record.get("citation key", "")
                if bib_keys and citation_key and citation_key not in bib_keys:
                    findings.append(Finding("error", section, label, "citation key", f"Citation key not found in BibTeX file: {citation_key}"))

    for record in sections.get("Open Gaps", []):
        for field, value in record.items():
            if normalize_key(value) not in NONE_VALUES and not is_bad_value(value, allow_na=True):
                findings.append(Finding("warning", "Open Gaps", "open-gaps", field, f"Open gap is not resolved: {value}"))

    return findings


def print_text_report(findings: list[Finding]) -> None:
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    print(f"Evidence manifest audit: {len(errors)} error(s), {len(warnings)} warning(s)")
    for item in findings:
        location = f"{item.section}"
        if item.record:
            location += f" / {item.record}"
        if item.field:
            location += f" / {item.field}"
        print(f"- {item.severity.upper()}: {location}: {item.message}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit a research-paper evidence manifest.")
    parser.add_argument("--manifest", required=True, help="Path to evidence_manifest.md")
    parser.add_argument("--root", default=".", help="Root directory used to resolve relative artifact paths")
    parser.add_argument("--bib", help="Optional BibTeX file used to verify citation keys")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Exit nonzero when warnings are present")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = Path(args.manifest)
    root = Path(args.root)
    bib = Path(args.bib) if args.bib else None

    if not manifest.exists():
        print(f"Manifest not found: {manifest}", file=sys.stderr)
        return 2
    if bib and not bib.exists():
        print(f"BibTeX file not found: {bib}", file=sys.stderr)
        return 2

    findings = check_manifest(manifest, root, bib)
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2, ensure_ascii=False))
    else:
        print_text_report(findings)

    if errors or (args.warnings_as_errors and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
