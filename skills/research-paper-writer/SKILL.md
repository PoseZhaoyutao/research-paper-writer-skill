---
name: research-paper-writer
description: Use when the user asks to generate, revise, polish, review, or prepare a research paper, manuscript, thesis-style paper draft, LaTeX/PDF/Word paper, or asks to turn experiment session memory, logs, metrics, artifacts, or session IDs into a paper draft, including "写论文", "论文初稿", "论文级文章", "精修论文", "审稿", or "根据会话生成论文".
---

# Research Paper Writer

## Overview

Use this skill to turn session memory, experiment records, code logic, metrics, figures, previous manuscripts, and user ideas into a complete research paper draft, then push it toward submission readiness through a real multi-agent paper team. A request such as "写论文" or "根据会话生成论文初稿" must start by creating the team, gathering evidence for the team, collecting each role's independent output, then writing, revising, polishing, and exporting deliverables only after the required role gates are satisfied.

## Non-Negotiable Agent Formation

This skill is a multi-agent workflow. Single-agent paper writing is invalid.

For every paper-generation, revision, polishing, review, submission-preparation, or session-memory-to-paper task, the first workflow phase must be `Stage 0 - Real Multi-Agent Team Formation`.

Before writing, rewriting, polishing, reviewing, or substantively editing any manuscript content, create active, distinct agents for these required roles. A still-active agent from the same current task may be reused only after being re-briefed and returning current-task-specific output; never reuse stale conclusions from a prior task or session.

- `main worker`: evidence recovery, manuscript state diagnosis, evidence ledger, outline, draft/revision implementation, figure/table/formula/reference integration.
- `journal editor`: publishability, title/abstract/framing, novelty, contribution, structure, related-work positioning, venue fit, reader flow.
- `domain reviewer`: technical truthfulness, method, formulas, experiment protocol, statistics, figures, tables, conclusions, limitations, and citation-to-claim support.

The coordinator must not silently serve as any required role. A "real agent" means a separately dispatched agent/subagent with its own prompt and returned role output. Simulating roles inside one response, using an internal checklist, or letting the coordinator impersonate a role is invalid.

If agent creation is unavailable, blocked, rejected, or the user asks to skip agents, stop before drafting/revision/review and report that the paper workflow is blocked because the required multi-agent team could not be created. Do not downgrade to single-agent writing, editing, reviewing, polishing, or formatting.

Add the optional `copy editor / formatting checker` agent before finalization when the user asks for language/format checking, when Word/LaTeX/PDF export is required, or when a venue/template/style guide is provided.

### Startup Gate

The first operational phase after loading this skill is `Stage 0 - Real Multi-Agent Team Formation And Prewriting/Prerevision Review`.

Allowed before creating agents: clarify the minimum thesis/venue/language decision if truly necessary, identify candidate files to brief agents, and inspect only enough context to build the agent prompts.

Forbidden before required agents are created and have returned role outputs:

- drafting new manuscript prose;
- rewriting an existing manuscript;
- giving a coordinator-only review verdict;
- polishing language;
- changing claims, figures, tables, formulas, references, or conclusions;
- declaring the paper direction ready;
- exporting final deliverables.

Each required agent must return a role-specific output before drafting or revision begins:

- main worker: manuscript state, evidence ledger, thesis proposal, section outline, figure/table/formula/reference plan, evidence gaps.
- journal editor: prewriting or prerevision decision, blocking issues, major issues, minor issues, and comments on framing, novelty, structure, venue fit, and missing narrative elements.
- domain reviewer: prewriting or prerevision decision, blocking issues, major issues, minor issues, evidence concerns, and comments on evidence sufficiency, technical risks, method/formula validity, experiment validity, and unsupported claims.

Only after all of the following are true may the main worker draft or modify manuscript content:

- the main worker has returned the manuscript state, evidence ledger, thesis/outline or prerevision packet, evidence gaps, and figure/table/formula/reference plan;
- the journal editor has returned its decision and issue list;
- the domain reviewer has returned its decision and issue list;
- reviewer outputs were produced independently, without leaking one reviewer's conclusions into the other's prompt;
- no `revise-evidence`, `rescope`, or `not-publishable-yet` decision remains unresolved.

## First Moves

1. Treat paper writing as evidence synthesis by a required paper team, not free writing by the coordinator.
2. Create the required agents immediately after the minimum briefing context exists; do not wait until after a draft is written.
3. Follow the workspace instructions for commands and data access. Always inspect exit code, stdout, and stderr for any command used as evidence.
4. Run the helper from the workspace root to locate recent source material:
   `python skills\research-paper-writer\scripts\collect_paper_context.py --root <workspace-root> --limit 30`
5. If the user gives a Codex session/thread ID, rerun with `--session-id <id>` and use session memory as a discovery source for locating evidence:
   `python skills\research-paper-writer\scripts\collect_paper_context.py --root <workspace-root> --session-id <id> --snippets 1200`
6. If the user names a topic, satellite, stage, artifact, or date, rerun with `--query`.
7. Read only the relevant session summaries, recent reports, LaTeX/PDF/Word outputs, experiment summaries, generator scripts, and code paths before drafting.

Load `references/paper_prompt_reference.md` for the required writing stages and formatting rules. Load `references/project_report_patterns.md` only when the current workspace is GNSSDataS or when those examples help interpret a similar experiment-paper workflow.

Load these role references before dispatching review agents:
- `references/agent_prompt_templates.md` before creating Stage 0 agents or any later review/revision agents.
- `references/journal_editor_review.md`
- `references/domain_reviewer_review.md`
- `references/copy_editor_review.md` when copy editing is requested or useful.
- `references/review_round_template.md` when recording review rounds.
- `references/evidence_manifest_template.md` before the first independent review round.
- `references/venue_brief_template.md` when a target venue, format guide, template, Word/PDF instruction file, or venue website is involved, and when preparing copy-edit/export checks.
- `references/adversarial_validation_scenarios.md` when testing or refining the skill itself.

## Session Memory To Paper Draft

Use this path when the user provides a session ID, says "读取会话记忆", or asks for a draft from experiment work.

1. Recover the memory sources: rollout JSONL, rollout summary, long-term memory files, lab notes, experiment logs, and any cited reports/artifacts. Do not claim hidden transcript access; name the files actually read.
2. Extract an experiment-to-paper ledger:
   - user goal, research question, and intended thesis;
   - domain, dataset, model/method, and evaluation target;
   - completed experiments, commands, and verification status;
   - raw artifacts, reports, figures, tables, logs, notebooks, and manuscript files;
   - sample counts, methods, baselines, metrics, splits, filtering rules, ablations, uncertainty, and missing data;
   - successful results, negative results, failure modes, and tool limitations;
   - user wording preferences such as "真实跑下去", "最终总结论文", "明确贡献与创新", and "读取之前的论文后进行修正".
3. Turn the ledger into claim tiers:
   - verified contribution: supported by landed artifacts and passing checks;
   - bounded interpretation: supported but sensitive to sample, horizon, satellite family, or protocol;
   - limitation/failure: negative transfer, unavailable truth, timeout, missing command access, or failed export;
   - next innovation: follow-up mechanism or conditional model suggested by evidence.
4. Read the latest prior manuscript before rewriting. For LaTeX lineages, inspect the newest `.tex`, `.aux`, `.log`, and PDF when available. For Word or Markdown lineages, inspect the newest `.docx`, `.md`, `.pdf`, and generator script. Create `revisedN` or a dated draft; do not overwrite the source-of-truth manuscript.
5. After Stage 0 required role outputs and gate approval, generate an actual paper draft, not a plan. If evidence is incomplete, keep academic placeholders only where the ledger marks work as pending.

## Autonomous Completion Rules

When the user asks for a paper from memory or experiment records, do the following without waiting for extra prompting when local evidence is available:

- recover the latest relevant session(s), not only the ID the user pasted if follow-up sessions clearly continued the same study;
- identify the newest verified artifact set, previous manuscript lineage, and the strongest defensible claim;
- compute missing summary tables or figures from existing raw outputs when the calculation is straightforward and reproducible;
- revise outdated prose when later experiments invalidate earlier claims;
- preserve negative results and protocol changes as part of the contribution, not as clutter to hide;
- after Stage 0 gate approval, generate a complete first draft even when some future experiments remain, while marking only the truly unresolved parts;
- prefer the project's existing manuscript style, directory structure, and generators over inventing new ones;
- stop and ask one concise question only when a missing user decision changes the thesis, venue, language, or required manuscript format.

## Draft State Routing

Choose the entry point from the current manuscript state:

- If no complete paper exists yet, run `Stage 0 - Team Formation And Prewriting Review`, then create `Stage 1 - Initial Draft` only after required role outputs are received.
- If a complete manuscript already exists, or the user asks to revise an existing paper, run `Stage 0 - Team Formation And Prerevision Review`, skip first-draft generation, and start directly with independent review before any edits.
- If the manuscript is partial, run `Stage 0`, let the main worker diagnose missing sections, obtain editor and reviewer agreement on the gap plan, then close the missing sections.

Even when a manuscript already exists, create agents first. Do not "quickly inspect and fix" the paper before the required agents return prerevision output.

Do not rewrite an already formed paper from scratch unless the user explicitly asks for a restart.

A `complete manuscript` contains at least: title, abstract, introduction, related work, methods, experiments, results, discussion or limitations, conclusion, references, figures/tables, and a traceable evidence registry.

## Multi-Agent Paper Loop

Always use real independent agents for this skill. The main thread remains the coordinator. The `main worker`, `journal editor`, and `domain reviewer` must all be distinct agents; the coordinator orchestrates them rather than doubling as the worker. Do not downgrade to a simulated, internal, or single-agent review.

### Required Roles

- `main worker`: recover context, build the evidence ledger, write missing sections, create figures/tables, integrate feedback, and own the final manuscript.
- `journal editor`: judge whether the work reads like a publishable paper: title, abstract, framing, novelty, contribution, structure, related-work placement, and reader flow.
- `domain reviewer`: audit technical truthfulness: method, formulas, experiments, statistics, figures, tables, conclusions, limitations, and references.

### Optional Role

- `copy editor / formatting checker`: inspect language, consistency, figure/table numbering, cross-references, citation style, and LaTeX/Word/PDF layout.

Before Stage 2, create a `venue brief` using `references/venue_brief_template.md`. Resolve it from, in order:
- explicit user instructions;
- user-provided conversation notes;
- user-provided Word/PDF/template files that specify formatting;
- the target journal or conference website and official author instructions;
- if no venue is known, a clearly labeled generic field-appropriate fallback.

### Two-Stage Delivery

0. `Stage 0 - Team Formation And Prewriting/Prerevision Review`
   - Required for every invocation of this skill.
   - Dispatch the main worker, journal editor, and domain reviewer as distinct agents before any manuscript drafting or editing.
   - For a new paper, the main worker first creates the evidence ledger, thesis proposal, and outline; the editor and reviewer evaluate those before drafting.
   - For an existing paper, the main worker first creates the manuscript/evidence review packet; the editor and reviewer evaluate it before revision.
   - If the copy editor is needed, dispatch it after the venue brief exists so it can prepare a format checklist before final polishing.
1. `Stage 1 - Initial Draft`
   - Use only when no complete manuscript exists yet.
   - The main worker creates a complete first draft only after Stage 0 required outputs are received.
2. `Stage 2 - Submission-Ready Revision`
   - If a complete manuscript already exists, start here after Stage 0 prerevision output is returned.
   - Dispatch the journal editor and domain reviewer as independent agents with the manuscript, evidence ledger, mandatory evidence manifest, venue brief, prior review packet when applicable, and their role brief.
   - If either reviewer returns a non-accept decision, the main worker must produce a revision note, update the manuscript or evidence package as appropriate, and resubmit to both reviewers.
   - When both required reviewers return `accept`, optionally dispatch the copy editor. If the copy editor returns a non-accept decision, the main worker fixes the manuscript and resubmits as needed.

### Review Contract

Each reviewer must return:
- `decision`: `accept`, `revise-manuscript`, `revise-evidence`, `rescope`, or `not-publishable-yet`;
- `blocking issues`;
- `major issues`;
- `minor issues`;
- `closed issues from prior rounds`;
- `evidence concerns`;
- `recommended changes`.

The main worker must return after each round:
- what changed;
- which comments were accepted;
- which comments were rejected and why;
- what evidence supports the revision;
- which issues remain unresolved.

Rejected reviewer comments remain open until that reviewer accepts the rebuttal or the user explicitly adjudicates the disagreement.

Do not declare the paper complete until:
- every required reviewer returns `accept`;
- there are zero blocking issues;
- there are zero unresolved evidence gaps affecting current claims;
- all final artifacts are verified.

### Dispatch Guidance

- Because independent review agents are mandatory, dispatch the `journal editor` and `domain reviewer` in parallel whenever their required inputs are ready.
- Give each reviewer only the manuscript, evidence ledger, evidence manifest, venue brief, relevant artifacts, prior review packet when applicable, and that reviewer's role brief.
- Do not leak the other reviewer's conclusions into a reviewer's prompt before they issue their own judgment.
- Use the optional copy editor only after the required reviewers both accept the science and structure.
- If the copy editor requests any change that alters science, claims, figures, tables, references, or structure, send the revised manuscript back through the journal editor and domain reviewer before final acceptance.

### Evidence Manifest Requirement

Before the first independent review round, create an `evidence manifest` using `references/evidence_manifest_template.md`. Reviewer acceptance is invalid if the manifest is missing or incomplete.

Run the audit helper before reviewer acceptance whenever local artifact paths are available:

`python skills\research-paper-writer\scripts\audit_evidence_manifest.py --manifest <evidence_manifest.md> --root <artifact-root>`

If a BibTeX file exists, include it:

`python skills\research-paper-writer\scripts\audit_evidence_manifest.py --manifest <evidence_manifest.md> --root <artifact-root> --bib <references.bib>`

Treat any audit error as a blocking evidence issue. Warnings require explicit acknowledgement or resolution before finalization.

## Evidence Integrity Rules

The manuscript must be auditable. Do not fabricate, embellish, or silently smooth over missing evidence.

- Every figure must trace to raw data or a reproducible generation script. Check axes, units, legends, sample counts, and caption claims against the source artifact.
- Every table must trace to a source CSV/TSV/database query or a reproducible calculation. Recompute all headline metrics before reuse.
- Every experimental analysis paragraph must be supported by the cited result table, figure, log, or verified calculation. State uncertainty, sample size, baseline, and failure cases where relevant.
- Every formula must either match the implemented method or be backed by a real source. Define all symbols, keep units consistent, and do not introduce decorative equations that are absent from the method.
- Every conclusion must be no stronger than the evidence. Separate verified findings, bounded interpretations, negative results, and speculation/future work.
- Every reference must be real. Reuse verified bibliography entries when possible; otherwise verify title, authors, venue, year, and DOI/arXiv/publisher record before adding it. Prefer primary sources, publisher pages, DOI metadata, arXiv records, or official repositories. Also verify that the cited source actually supports the sentence attached to it. Never cite a paper you have not verified, and never invent bibliographic details.
- If a claim, value, equation, figure, table, or reference cannot be verified, mark it as pending, remove it, or ask for the missing evidence. Do not guess.

## Default Workflow

Do not begin this workflow as a single coordinator. The coordinator may gather candidate artifacts, but the `main worker` owns the evidence ledger and manuscript implementation, while the `journal editor` and `domain reviewer` gate the direction before prose changes.

### 0. Team Formation Gate

Create or re-brief the required agents using `references/agent_prompt_templates.md` and obtain their Stage 0 outputs before continuing. For a pure review task, the main worker prepares the manuscript/evidence packet, the editor and reviewer independently review it, and the coordinator only synthesizes their returned judgments.

### 1. Evidence Ledger

Have the main worker build a short ledger of source files and what each contributes: previous manuscript/report, latest experiment tables, figures, logs, notebooks, generator scripts, code implementation, and unresolved gaps. Prefer newest non-superseded artifacts when the user asks for "最新".

Do not invent results. If a number is not present in source material, either compute it from local artifacts or mark it as pending in academic wording.

If a session memory says a job was started but not verified, inspect the referenced logs/CSVs before using the result. Never turn an unverified background process, smoke run, or failed command entry into a paper claim.

Session memory is a locator, not final evidence. Every factual or quantitative manuscript claim must resolve to raw artifacts, logs, reproducible calculations, run metadata, or verified external sources.

### 2. Unified Modeling Note

Before prose, extract:
- research objective and object;
- method line that matches code;
- key variables, symbols, units, formulas, and metrics;
- datasets, sample selection, baselines, horizons or test conditions, and evaluation protocol;
- what is implemented now versus future work.

For memory-driven drafts, also extract the paper thesis in one paragraph: why the experiment matters, what was newly verified, what failed, and how that changes the contribution.

### 3. Detailed Outline

After the editor and reviewer have returned Stage 0 output, create the paper frame with these sections unless the user requests another structure:
- 背景/引言
- 相关工作
- 方法论述
- 实验设计
- 实验结果与分析
- 机制讨论或适用性边界
- 总结

Include proposed formula list, table list, figure list, and expected deliverables.

For a thesis/paper initial draft, prefer a complete manuscript skeleton: title, abstract, keywords, introduction/background, related work, method, experiment design, results, mechanism/discussion, limitations/applicability boundary, conclusion, references, table list, figure list.

### 4. Draft

After Stage 0 gate approval, have the main worker write an academic draft in the user's requested language, defaulting to Chinese if the conversation is Chinese. Make it structurally stable and logically self-consistent. Explain every numbered formula, define metrics before using them, and keep method claims aligned with actual code and artifacts.

### 5. Paper-Level Revision

After Stage 0 prerevision output, revise for thesis strength: sharpen contribution, related-work positioning, mechanism explanation, limitations, and evidence hierarchy. Separate robust claims from hypotheses and future work.

When updating an existing manuscript, revise claims in place: abstract, contribution paragraph, experiment tables/figures, discussion, limitations, and conclusion must all agree with the newest verified evidence. Preserve older versions by copying to the next `revisedN` file or a dated output directory.

### 6. Integrity Audit

Before polishing or export, build a compact audit map:

- figure registry: figure id -> raw data -> generation script/command -> output file -> sample set -> key claim;
- table registry: table id -> raw data -> calculation script/command -> output file -> metrics -> key claim;
- formula registry: equation id -> exact implementation/source -> code revision/config/checkpoint/seed -> symbol definitions;
- claim registry: major conclusion -> supporting figure/table/artifact/log;
- reference registry: citation key -> verified bibliographic source -> exact claim supported;
- run registry: result id -> command -> data version -> code revision -> config -> seed -> environment -> output artifact.

Resolve every unsupported item before treating the draft as complete.

When the manifest is written, run `scripts/audit_evidence_manifest.py` and attach its result to the review packet. Do not treat the script as a substitute for expert review; use it as a hard preflight for missing fields, missing local artifacts, unresolved statuses, and missing BibTeX keys.

### 7. Post-Draft Review Rounds

Run the role loop described above. Preserve a concise paper-formation log with:
- draft version;
- reviewer decisions;
- accepted/rejected comments;
- manuscript changes;
- remaining risks.

If reviewers determine the manuscript needs more evidence, more experiments, or a narrower thesis, do not keep polishing prose. Route the work to `revise-evidence`, `rescope`, or `not-publishable-yet` instead.

### 8. Polish And Export

By default produce all of:
- `.docx` Word manuscript;
- `.tex` LaTeX source;
- `.pdf` compiled or rendered output.

Reuse existing project paper/report generators when the topic matches. Otherwise create a scoped generator or manuscript files under a clear output path such as `output/doc/<topic-date>/`, `output/latex/<topic-date>/`, or the project's established manuscript directory. Use `python-docx` for Word, a suitable LaTeX class for the language/domain, and `xelatex`, `latexmk`, or an existing PDF generation path for PDF. If one export tool is unavailable, still leave the other completed files and report the exact failing command.

When the task is only "论文初稿版", at minimum produce a complete Markdown or LaTeX draft with abstract, body, tables/figures placeholders or generated assets, and references. Export Word/PDF afterward when tools are available.

### 9. Verification Gate

Before claiming completion:
- confirm the required `main worker`, `journal editor`, and `domain reviewer` agents were created before drafting or revision, and their Stage 0 outputs are recorded;
- confirm the venue brief exists or that a generic fallback was explicitly chosen;
- confirm the evidence manifest audit was run, or explain why no local artifact-root audit was possible;
- verify output files exist and have nonzero size;
- inspect LaTeX or PDF generation logs when applicable;
- check formulas are numbered and referenced consistently;
- check variables, vector/matrix style, and units;
- check tables are three-line style or described as such;
- check figures have axis labels with units and no unsupported visual claims;
- check figure/table values against their source artifacts or generation scripts;
- check experimental analysis against the actual tables, plots, logs, and sample counts;
- check conclusions do not exceed verified evidence;
- check references are real, verified, and style-consistent;
- confirm no unsupported experimental values were introduced.
- confirm session-memory-derived candidate claims are backed by artifacts, logs, reproducible calculations, run metadata, or verified external sources rather than memory alone.

## Red Flags

If any of these happen, stop and repair the workflow before continuing:

- the coordinator starts drafting before required agents exist;
- reviewers are introduced only after a draft is already written;
- the main worker, editor, or reviewer roles are simulated in one response instead of being distinct active agents;
- a complete or partial existing manuscript is "quickly fixed" before required agents return prerevision output;
- an existing manuscript is edited before editor/reviewer prerevision output is returned;
- a copy editor changes claims, figures, tables, formulas, references, or structure without sending the manuscript back to the editor and reviewer;
- agent creation fails and the coordinator continues as if the role loop happened.

## Paper Standards

Core formatting defaults:
- title: 二号黑体, centered for Word; clear title block for LaTeX;
- first-level headings: 四号宋体, not bold in Word-style drafts;
- second-level headings: 五号楷体, bold;
- body: 五号宋体, first-line indent 2 Chinese characters;
- tables: three-line style, 小五号宋体;
- figures: 图宽 7.5 cm when targeting Word-style manuscript, no grid, distinct line styles;
- axis labels: `变量符号/单位` or `变量名称/单位`; degrees as `(°)`, other units without parentheses;
- physical scalar variables italic, units upright, vectors and matrices bold italic.

Use local prior reports as style examples, but do not copy stale claims into new reports without checking the latest artifacts. Treat project-specific references as adapters, not universal rules.

## Final Response

When finished, provide:
- paths to `.docx`, `.tex`, and `.pdf`;
- 3-6 key source files used;
- verification commands/results;
- a short integrity audit summary covering figures, tables, formulas, conclusions, and references;
- a concise multi-agent review summary with the final decisions of the journal editor, domain reviewer, and optional copy editor;
- a short startup-gate summary listing the required agents created and when they returned Stage 0 outputs;
- any missing export or evidence gaps.
