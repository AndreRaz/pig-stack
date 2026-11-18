---
name: pig-swarm
description: "Trigger: pig-swarm, /pig-swarm, parallel workers, fan out slices. Opt-in parallel workers over disjoint edit paths with one seam check."
license: MIT
metadata:
  author: pig-stack
  version: "1.2"
  layer: "3"
disable-model-invocation: true
---

## Activation Contract

Load only when the user invokes `/pig-swarm` or explicitly requests parallel fan-out when the ODD Writer trigger holds: 2+ independent units of ~100+ changed lines each with disjoint files.

## Hard Rules

- Never fan out small or coupled work. Units under ~100 changed lines run inline, one after another.
- Every writing worker gets exact, non-overlapping `## Allowed edit paths` and an `## Invariants` list of shared helpers to reuse.
- The parent owns git. Workers never commit, format the whole repo, generate code, or install dependencies.
- Use isolated worktrees only when two units must touch the same file.
- Workers use `inherit-parent` unless `.pig-stack/models.md` sets `pig-swarm workers`.
- Respawn a worker at most once, only when its result lacks the evidence its brief required. A second miss is a recorded gap, never a pass.

## Decision Gates

| Shape | Setup |
|---|---|
| Read-only checks across slices | N read-only workers, each returning `PASS`, `ISSUES`, or `BLOCKED` with evidence. |
| Disjoint code units | N `pig-worker` calls in one turn, disjoint edit paths. |
| Units sharing a file | One worktree per unit. |

## Execution Steps

1. Write the done predicate, the slices, the shared invariants, and for races the selection rule (`first-pass`, `rank-all`, `best-of`).
2. Collect exact `SKILL.md` paths per slice with `skill-registry`.
3. Launch all workers in one batch with standalone briefs (`Spec:`, allowed edit paths, invariants, skills, verification commands).
4. Check every diff stayed inside its declared edit paths.
5. Run the Close Sequence once over the combined diff: `deslop`, then the full suite as the seam check.

## Output Contract

Return: a table of `Slice | Status | Evidence | Gaps`, proven issues, dropouts, and seam-check output.
