# GNSSDataS Project Report Patterns

Use this reference only as a GNSSDataS adapter when the current workspace is this project or when a similar orbit-dynamics paper needs examples. Do not treat these project-specific artifacts or claims as universal rules for the main skill.

## High-Value Prior Outputs

- `output/doc/初稿万源之源/drag_implicit_learning_s1_paper_draft.md`
  Early full Chinese draft with the "unified modeling -> formulas -> experiment analysis" style.
- `output/doc/sentinel1_ar1_paper_20260429/sentinel1_ar1_paper_formal.txt`
  Word-oriented formal paper text with abstract, keywords, formulas, tables, and figure captions.
- `output/latex/sentinel1_ar1_paper_20260429/sentinel1_ar1_paper_nature_revised5.tex`
  Mature Sentinel-1 LaTeX manuscript lineage.
- `output/latex/swarm_self_supervised_scale_report_20260512/swarm_self_supervised_scale_report.tex`
  Swarm self-supervised scale report with LaTeX table/figure conventions.
- `output/latex/swarm_network_scale_report_20260513/swarm_network_scale_report.tex`
  Latest Swarm network-scale report pattern with multi-method comparison and Stage52 generalization.
- `reports/32_final_paper_summary_2026-05-07/paper_summary_and_contributions.md`
  Good source for defensible paper framing and claim boundaries.
- `output/latex/sentinel1_ar1_paper_20260429/sentinel1_ar1_paper_nature_revised2.tex`
  Sentinel-1/3 real-Orekit revision that turns completed S3 negative-transfer evidence into paper claims.
- `output/latex/sentinel1_ar1_paper_20260429/sentinel1_ar1_paper_nature_revised3.tex`
  Adds Sentinel-6 and altitude-trend analysis; useful for separating absolute RMSE from relative gain collapse.
- `output/latex/sentinel1_ar1_paper_20260429/sentinel1_ar1_paper_nature_revised4.tex`
  Adds orbit-fraction endpoint experiment, figure/table update, and nuanced mechanism discussion.

## Useful Report Generator Scripts

- `scripts/15_build_sentinel1_ar1_word_paper.py`: Word/PDF formal Sentinel-1 paper builder.
- `scripts/16_build_latex_nature_sentinel1_paper.py`: LaTeX + figure generator for Sentinel-1 AR(1) paper.
- `scripts/47_make_self_supervised_latex_report.py`: self-supervised Swarm LaTeX report builder.
- `scripts/49_make_swarm_network_latex_report.py`: Swarm z(t) network-model LaTeX report builder.
- `scripts/51_make_swarm_batch_method_report.py`: batch-method report builder.
- `scripts/55_build_swarm_paper_experiment_ledger.py`: experiment ledger builder for paper completion work.

## Evidence Selection Rules

- Prefer `artifacts/` for raw computed outputs and `reports/` for interpreted summaries.
- Prefer `output/doc/` and `output/latex/` for previous manuscript style and mature wording.
- Prefer `docs/superpowers/specs/` and `docs/superpowers/plans/` for design intent and implementation scope.
- Prefer `.codex/memories/rollout_summaries/` and `raw_memories.md` only to discover what was done and where evidence landed; verify claims against cited project artifacts before writing final numbers.
- Treat files named `SUPERSEDED`, `smoke`, `partial`, or `probe` as lower-confidence unless the user specifically asks for them.
- When the user asks for "latest", compare modification times and concrete dates in filenames.
- Keep negative results and limitations. This project often has strong baselines and cross-satellite failure cases; do not overclaim.
- If command access was unavailable or a task was interrupted, report that state honestly and continue from referenced logs/artifacts instead of treating it as a completed experiment.

## Common Claim Shape

Strong reports in this project usually:
- define a physically injectable correction signal rather than a detached black-box predictor;
- compare against BaseProp, constant-scale baselines, LastScale, AR(1)-y, EWMA, MLP, GRU, or TCN as appropriate;
- separate Sentinel, Swarm, and other satellite-family conclusions;
- report horizon-specific behavior at 6 h, 24 h, 72 h, or the relevant configured horizon;
- distinguish true Orekit endpoint propagation from linearized or proxy evaluations;
- explicitly name sample counts, filtering criteria, and leakage boundaries.
- preserve manuscript lineage by producing `revised2`, `revised3`, etc., or a dated output directory instead of overwriting the prior paper.

## Memory-Derived Sentinel Paper Lessons

The session `019e01c8-5f50-7253-be35-9034c85e98e8` established report-writing rules that should carry forward:

- "把实验真实跑下去" means run or verify real Orekit endpoint experiments before paper claims; do not stop at an experiment memo.
- Read the prior paper source/aux before revising; update the manuscript itself when the user asks to revise the report.
- Split long Orekit jobs into restartable shards when tool windows are short, and state the shard/sample protocol in the paper.
- Contribution sections should separate verified contributions, limitations, negative transfer, and next-step innovation.
- For Sentinel-family drag-scale memory, avoid the claim "AR(1)-y universally wins": current evidence supports Sentinel-1 gains, Sentinel-3/Sentinel-6 negative transfer, weak S3-to-S1 same-epoch transfer, severe S6-to-S1 incompatibility, and orbit-phase effects that are secondary to horizon/error-accumulation effects.
