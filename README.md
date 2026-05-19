# Research Paper Writer Skill

`research-paper-writer` is a Codex skill for turning session memory, experiment logs, code artifacts, metrics, figures, and prior drafts into evidence-grounded research manuscripts.

The skill is designed for serious paper writing rather than lightweight report generation. It requires a real multi-agent workflow before manuscript drafting, revision, review, polishing, or export can begin.

## What It Does

- Recovers paper context from session IDs, experiment records, logs, scripts, figures, tables, manuscripts, and reports.
- Builds an auditable evidence ledger before using claims in the paper.
- Routes work through mandatory independent roles:
  - `main worker`
  - `journal editor`
  - `domain reviewer`
  - optional `copy editor / formatting checker`
- Provides reusable agent prompt templates for Stage 0, review, revision, and formatting roles.
- Provides a venue brief template for journal/conference/thesis formatting requirements.
- Provides an evidence manifest audit script for missing fields, missing local artifacts, unresolved statuses, and BibTeX key checks.
- Starts from review when a complete manuscript already exists.
- Checks figures, tables, formulas, conclusions, and references against real evidence.
- Supports Markdown, LaTeX, Word, and PDF-oriented paper workflows.

## Non-Negotiable Multi-Agent Gate

Single-agent paper writing is invalid for this skill.

Every paper-generation, revision, polishing, review, submission-preparation, or session-memory-to-paper task must begin with `Stage 0 - Real Multi-Agent Team Formation`.

Before drafting or modifying manuscript content:

1. Create or re-brief the required agents.
2. Collect current-task-specific outputs from each role.
3. Resolve any `revise-evidence`, `rescope`, or `not-publishable-yet` decisions.
4. Only then allow the main worker to draft or revise the manuscript.

If real agent creation is unavailable or the user asks to skip agents, the workflow must stop rather than simulate roles in one response.

## Repository Layout

```text
skills/
  research-paper-writer/
    SKILL.md
    agents/openai.yaml
    references/
      agent_prompt_templates.md
      venue_brief_template.md
    scripts/collect_paper_context.py
    scripts/audit_evidence_manifest.py
  research-report-writer/
    SKILL.md
    agents/openai.yaml
```

`research-paper-writer` is the canonical skill.

`research-report-writer` is a legacy compatibility alias that points users toward the paper-writing workflow.

## Installation

Copy the canonical skill into your Codex skills directory:

```cmd
xcopy skills\research-paper-writer %USERPROFILE%\.codex\skills\research-paper-writer\ /E /I /Y
```

Optionally install the legacy alias:

```cmd
xcopy skills\research-report-writer %USERPROFILE%\.codex\skills\research-report-writer\ /E /I /Y
```

Restart Codex after installation so the skill list reloads.

## Usage

In Codex, invoke:

```text
$research-paper-writer
```

Example requests:

```text
根据这个会话 ID 和实验记录生成论文初稿。
```

```text
读取已有 manuscript.tex，从审稿开始，按期刊要求修改到投稿版。
```

```text
帮我审这篇论文是否可投，检查图表、公式、实验分析、结论和参考文献是否可靠。
```

## Evidence Integrity Rules

The skill must not invent claims, references, metrics, formulas, figures, or tables.

Every manuscript claim should trace to one of:

- raw experiment artifacts;
- logs or reproducible commands;
- verified tables or figures;
- code implementation;
- prior manuscript lineage;
- verified external sources such as DOI, publisher, arXiv, or official documentation records.

If evidence is missing, the manuscript should mark the item as pending, remove the claim, narrow the conclusion, or ask for the missing source.

## Validation

The packaged skill has been checked with:

```cmd
set PYTHONUTF8=1&& python %USERPROFILE%\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\research-paper-writer
```

```cmd
python -m py_compile skills\research-paper-writer\scripts\collect_paper_context.py
```

```cmd
python -m py_compile skills\research-paper-writer\scripts\audit_evidence_manifest.py
```

Run an evidence manifest audit with:

```cmd
python skills\research-paper-writer\scripts\audit_evidence_manifest.py --manifest evidence_manifest.md --root .
```

If a BibTeX file exists:

```cmd
python skills\research-paper-writer\scripts\audit_evidence_manifest.py --manifest evidence_manifest.md --root . --bib references.bib
```

## License

No license has been specified yet. Add a license before publishing publicly if you want others to reuse or modify the skill.
