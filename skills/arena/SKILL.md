---
name: arena
description: "Trigger: arena, /arena, competing implementations, bakeoff. Opt-in competing candidates in isolated worktrees, rubric-scored and merged into one design."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "3"
disable-model-invocation: true
---

## Activation Contract

Load only when the user invokes `/arena`, or when `architect` returned an open prototype question about an expensive, hard-to-reverse design.

## Hard Rules

- Never start automatically for routine work.
- Each candidate works in its own worktree or `/tmp/arena-<slug>/candidate-<n>/`.
- Default to 2 candidates on `inherit-parent` with distinct strategy briefs. Use more models only when `.pig-stack/models.md` sets `arena runners`.
- One round only. If candidates diverge wildly, reframe the brief once and rerun; a second divergence goes to the user as a decision.
- Pick one base by rubric. Graft at most two ideas from the others by hand. Never paste fragments together.
- Delete losing worktrees before reporting.

## Decision Gates

| Situation | Action |
|---|---|
| Default budget | 2 candidates on `inherit-parent`, parent scores with the rubric. |
| `arena runners` configured | Configured runners plus one read-only judge from another vendor when available. |
| Candidates converge | Ship the shared shape, no graft. |

## Execution Steps

1. Write the artifact, 3-6 gradeable rubric criteria, and candidate output paths.
2. Spawn candidates in one batch with the same task, their own path, and a short rationale requirement.
3. Score each against the rubric and pick the simplest extensible base.
4. Graft at most two ideas, remove losing worktrees, then run the Close Sequence once (`deslop`, verification).

## Output Contract

Return: rubric scores, chosen base and reason, grafts with source, rejected parts, cleanup confirmation, and verification output.
