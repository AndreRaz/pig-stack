---
name: recall
description: "Trigger: recall, /recall, catch me up, where did I leave off. Rebuilds working state from odd/tasks, git, transcripts, and memory into a tight brief."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "6"
---

## Activation Contract

Load when starting or resuming work across sessions and the user asks to catch up or reconstruct state on a topic.

## Hard Rules

- **Live state beats stale memory:** Always reconcile `odd/tasks/*.md`, `git status`, `git branch`, and recent `git log` before trusting chat transcripts or memory notes.
- **Lock scope first:** Confirm topic, repository, and time window (default last 7 days). Never read unrelated project transcripts without permission.
- **Read-only:** Output the state brief only; do not modify code.

## Decision Gates

| Available Sources | Action |
|---|---|
| `odd/tasks/<feature>.md` + git exist | Reconcile specs, checked tasks, `## Log`, and `git diff` directly. |
| Broad multi-chat history needed | Inspect active workspace transcripts (`ls -t`) or Engram (`mem_context` / `mem_search`) via 1 `pig-explorer` when more than one read batch is needed. |

## Execution Steps

1. Check `git status`, active branches, `odd/tasks/`, and Engram memory (if available).
2. Inspect matching recent transcripts/PRs within the locked window.
3. Cross-check claimed completed items against actual `git log` / live state.
4. Synthesize the brief using `unslop`.

## Output Contract

Return:
- **Capsule:** <= 5 bullets on current state
- **Threads:** 1 line each tagged `[merged] | [open PR #N] | [in flight <branch>] | [verified, uncommitted] | [planned]`
- **Recurring Problems:** <= 5 items with prior failed attempts
- **Next Move:** single highest-leverage concrete step
