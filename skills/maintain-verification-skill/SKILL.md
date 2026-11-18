---
name: maintain-verification-skill
description: "Trigger: maintain-verification-skill, /maintain-verification-skill, audit verify skill. Syncs verify-<app> and its feature map against real app behavior."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "3"
---

## Activation Contract

Load when maintaining an existing `verify-<app>` skill and its `features/` map after product changes.

## Hard Rules

- **Edit scope:** Edit only the `verify-<app>/` directory (`SKILL.md`, `features/`, owned scripts). Never patch product bugs here; report product regressions separately.
- **Live pass mandatory:** Source inspection never replaces running `launch -> doctor -> drive -> cleanup` across every mapped feature.
- **Health and cleanup invariants:** Run `doctor` before driving and after any failed drive; preserve captured evidence after teardown.

## Decision Gates

| Drift Type | Action |
|---|---|
| Wrong user steps or missing feature | Update `features/` doc map (`doc drift`). |
| Harness script fails on working app | Fix harness script (`harness gap`) and re-drive live. |
| App behavior genuinely broken | Report `product regression` without weakening the feature test. |
| No `verify-*` skill exists | Stop and recommend `create-verification-skill`. |

## Execution Steps

1. Locate `verify-*/` and audit `features/README.md` against sibling files.
2. Inspect source entry points for each feature (fan out read-only if many) and recent churn for unmapped features.
3. Run live verification across all features, triaging `doc drift` vs `harness gap` vs `product regression`.
4. Confirm clean teardown and preserved evidence.

## Output Contract

Return: outcome (`clean | changed | blocked`), features verified, `doc drift` / `harness gap` fixes, `product regressions` found, and evidence paths.
