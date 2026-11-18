---
name: why
description: "Trigger: why is this built this way, /why, design rationale, regression history. Explains motivation from git commits, PR history, and docs."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "1"
---

## Activation Contract

Load when explaining why code, thresholds, constraints, or workarounds exist, or tracing when a regression was introduced.

## Hard Rules

- **Record over speculation:** Answer from git commits (`git log -S`, `git log -L`, `git blame`), PR descriptions, and repo docs, not guesses from current code alone.
- **Separate fact from inference:** Quote or cite commit SHAs, PR numbers, and authors directly. Label any extrapolation as `[inferred]` and explicitly name what the record does not answer.
- **Strictly read-only:** Never modify files or history.

## Decision Gates

| Question Need | Source Command |
|---|---|
| Origin of a symbol or constant | `git log -S "<symbol>" -p -n 5` |
| Evolution of a specific line range | `git log -L <start>,<end>:<path>` |
| Missing git trail (squashed/external) | Inspect docs, `odd/tasks/`, or issue/PR references via `gh` if available. |

## Execution Steps

1. Locate the exact lines/symbols in the current tree.
2. Trace introducing and modifying commits in git history (plus linked PR discussions if accessible).
3. Summarize original intent, subsequent pivots, and any unresolved gaps.

## Output Contract

Return: cited timeline (SHA/date/author/intent), confirmed rationale, `[inferred]` bridges (if any), and unanswered gaps.
