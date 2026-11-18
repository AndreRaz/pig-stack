---
name: technical-writing
description: "Trigger: technical-writing, /technical-writing, write readme, PR description, commit message, RFC. Applies Diataxis structure and PR/commit formats."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "1"
---

## Activation Contract

Load when writing or reviewing READMEs, RFCs, guides, PR descriptions, or commit messages.

## Hard Rules

- One Diataxis mode per document: tutorial, how-to, reference, or explanation. Link instead of mixing.
- One instruction per sentence, imperative mood, real symbol and command names.
- Run `unslop` once on the final text. Do not restate its rules here.
- Commits: Conventional Commits `type(scope): subject`, no AI attribution.
- PR body: at most 40 lines, headings in this order and dropped when empty: `Why`, `What changed`, `Scope`, `Tradeoffs`, `Blast Radius`, `Verification`. Link long logs.
- Every path, count, and command matches the repository at the commit that lands it.

## Decision Gates

| Artifact | Rules |
|---|---|
| Doc, README, RFC | One mode, verified links. |
| PR description | 40-line cap, ordered headings, observed verification output. |
| Commit message | Conventional Commit, optional short body with the reason. |

## Execution Steps

1. Pick the mode and the reader.
2. Draft from observed facts and real names only.
3. Run `unslop`, then check every referenced path and command exists.

## Output Contract

Return the artifact or a diff summary, with the chosen mode.
