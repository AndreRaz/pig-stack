---
name: show-me-your-work
description: "Trigger: show-me-your-work, /show-me-your-work, decision log, audit trail. Maintains an append-only TSV decision log for long or unattended runs."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "4"
---

## Activation Contract

Load when running long, multi-phase, or unattended work that needs a compact, auditable TSV trail (`decisions.tsv` or `.audit/<slug>.tsv`).

## Hard Rules

- **Append-only TSV:** Never edit or delete past rows; supersede a wrong call with a new row explaining what happened.
- **Concrete evidence pointers:** Every row cites a commit SHA, `file:line`, test output path, or artifact path—never prose paragraphs.
- **Unslopped plain words:** Write `decision` and `why` like telling a teammate (`unslop`), escaping spreadsheet formula prefixes via `scripts/log.sh`.
- **Audit before handoff:** Cross-check this session's rows against actual tool outputs and `git log`; log any unrecorded pivot or missing evidence as a superseding row.

## Decision Gates

| Condition | Target Location |
|---|---|
| Normal in-progress tracking | Local `decisions.tsv` or `.audit/<task-slug>.tsv` (uncommitted by default). |
| High-risk or unattended PR needing reviewer trust | Commit `.audit/<task-slug>.tsv` alongside the PR when authorized. |
| Resuming an existing log | First row of the new run uses `phase: start` naming prior timestamp range. |

## Execution Steps

1. Initialize or inspect the TSV using `references/decision-log-template.tsv`.
2. Append a row at forks, completed units, pivots, reverts, or blockers with `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`.
3. Before closing, verify every row's evidence path/SHA resolves on disk or in git.

## Output Contract

Return: log file path, row count added this run, any superseded rows/gaps found during audit, and final verification state.

## References

- [references/decision-log-template.tsv](references/decision-log-template.tsv) — canonical TSV header (`ts`, `phase`, `decision`, `why`, `evidence`, `result`).
- [scripts/log.sh](scripts/log.sh) — append helper sanitizing tabs, newlines, and formula prefixes.
