# Paper Prompt Reference

Use this reference when the task is to draft, update, polish, or export an academic paper from session memory, experiment records, or prior manuscripts.

## Required Stages

1. Extract and unify the research target, research object, method line, key variables and symbols, existing formulas and their purpose, and code-implemented method. Output this as a modeling note before writing the body.
2. When the source is an experiment session memory, first build a ledger of user goal, completed experiments, artifacts, commands, verification, failures, and unresolved gaps. Convert that ledger into verified contributions, bounded interpretations, limitations, and next-step innovations.
3. Generate a detailed outline with title, abstract points, keywords, major sections, subsection points, formula list, table list, and figure list.
4. Write the manuscript body. Default structure: 引言/背景, 相关工作, 方法, 实验设计, 实验分析, 机制讨论/适用性边界, 结论/总结. For project reports, the six-section structure 背景, 相关工作, 方法论述, 实验设计, 实验分析, 总结 is preferred.
5. Self-check and revise: symbol consistency, formula-method alignment, loss-function/code alignment, metric definitions, section transitions, academic tone, and unsupported numerical claims.
6. Export a complete Word, LaTeX, and PDF version unless the user explicitly asks for text only.

## Memory-Driven Draft Requirements

- A session ID is not enough by itself: read the rollout summary and cited artifacts before using numbers in the draft. Session memory may suggest candidate claims, but it is not sufficient evidence on its own.
- Preserve the user's research intent. Phrases such as "真实跑下去", "最终总结论文", "明确贡献与创新", and "读取之前的论文后进行修正" mean the output should be a manuscript revision grounded in real experiments.
- If the prior session reports a completed experiment, verify the named CSV/report/log when available. If the prior session only says a process was started, write it as pending until final artifacts are inspected.
- Use negative results as evidence. Failed transfers, degraded ablations, sample sensitivity, missing data, and timeout-induced protocol changes belong in the paper's limitations or applicability-boundary discussion.
- When revising an existing paper, keep the lineage traceable: read the latest source, create the next `revisedN` or dated draft, and update abstract, contribution, result tables/figures, discussion, and conclusion consistently.

## Writing Requirements

- Prefer stable structure, symbol consistency, logical self-consistency, and formula correctness over ornate prose.
- Include meaningful formulas for the actual method only when they match the current code, experiment design, or a verified external source.
- Number formulas continuously.
- Explain every formula after it appears.
- Keep method descriptions consistent with actual scripts, model code, and experiment artifacts.
- Experimental analysis must discuss trends, comparison baselines, sample counts, uncertainty, limitations, and failure cases.
- References must be real, credible, and style-consistent. Do not invent bibliographic details.
- Contribution writing must separate what is verified, what is only a bounded interpretation, and what remains a future innovation direction.

## Truthfulness Review

Run this review before finalizing the manuscript:

### Figures

- Confirm each figure comes from real data or a reproducible generation script.
- Check plotted values, axes, units, legends, error bars, and captions against the source artifact.
- Do not use a schematic, smoothed curve, or illustrative trend as experimental evidence unless it is explicitly labeled as schematic.

### Tables

- Confirm each table value comes from a real source file or reproducible calculation.
- Recompute important aggregates such as mean, median, RMSE, CI, percentage gain, and sample counts when feasible.
- Do not merge incompatible protocols into one table without saying so.

### Experimental Analysis

- Tie every paragraph-level claim to a real table, figure, artifact, or verified calculation.
- Report baselines, sample counts, filtering, evaluation split, uncertainty, negative results, and missing data that materially affect the claim.
- If two artifacts disagree, resolve the conflict or write the uncertainty explicitly.

### Formulas

- Keep only equations that describe the actual method, loss, metric, or cited theory used in the paper.
- Define every symbol at first use, keep units consistent, and ensure formula text matches the implementation.
- If a formula is borrowed from literature, cite a real source. If it is inferred from code, state it in a form that the code actually implements.

### Conclusions

- Each conclusion must be supported by the strongest verified evidence available.
- Do not generalize beyond the tested data regime, sample set, horizon, domain, or benchmark.
- Separate verified findings, bounded interpretations, and future hypotheses.

### References

- Reuse verified references from prior manuscripts or bibliography files when possible.
- For any new citation, verify title, authors, venue, year, and DOI/arXiv/publisher record from a reliable source before adding it. Prefer primary sources, DOI metadata, publisher pages, arXiv records, or official repositories.
- Verify not only that the source exists, but that it supports the specific sentence it is attached to.
- If a citation cannot be verified, omit it or mark it pending. Never invent author lists, venues, years, page numbers, DOI, or arXiv IDs.

## Initial Paper Draft Shape

A "论文初稿版" should be a complete draft, not a writing plan:

- 标题, 摘要, 关键词;
- 引言/背景 with the problem, gap, and contribution;
- 相关工作 with credible categories and no fabricated bibliographic details;
- 方法 with variables, formulas, assumptions, and code-aligned implementation;
- 实验设计 with data source, arc selection, baselines, horizons, metrics, and leakage controls;
- 实验分析 with tables/figures, trends, negative results, sample counts, uncertainty, and failure cases;
- 机制讨论 or 适用性边界 when evidence shows regime differences;
- 结论 with verified contributions, limits, and next-step innovation.

## Paper Construction Rules

- Infer the manuscript type from the user's goal and prior artifacts: project report, conference-style draft, journal-style paper, thesis chapter, or revision of an existing manuscript.
- Infer the paper's central claim only after the evidence ledger is built. If the evidence supports multiple weaker claims rather than one strong claim, write that honestly.
- Every major claim should be traceable to at least one source category: artifact table/figure, log, code path, prior manuscript, or verified calculation.
- If experiments are incomplete, produce the strongest truthful draft now and mark only the genuinely missing evidence as pending.
- Prefer a contribution paragraph that answers: what was built, what was verified, what boundary was discovered, and why that changes prior understanding.
- Keep a compact provenance map for figures, tables, formulas, major claims, and references so the draft can be audited later.
- Before submission-style review, produce a venue brief from user instructions, provided templates/documents, official venue guidance, or a clearly labeled generic fallback.

## Chinese Word-Oriented Formatting Defaults

- 标题：二号黑体，居中。
- 一级标题：四号宋体，不加粗。
- 二级标题：五号楷体，加粗。
- 正文：五号宋体，不加粗，首行缩进 2 字符。
- 表：三线表，小五号宋体。
- 图：图宽 7.5 cm，无网格线，不同线型区分。
- 坐标轴标目：`变量符号/单位` 或 `变量名称/单位`；度写为 `(°)`，其他单位不加括号。
- 物理变量符号用斜体，单位用正体，矢量和矩阵用黑斜体。

## Output Discipline

The final manuscript should be a complete paper/report, not an explanation of how to write one. Preserve academically worded placeholders such as "后续实验补充" only when evidence is truly pending.
