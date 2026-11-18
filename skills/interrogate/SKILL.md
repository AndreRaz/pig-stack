---
name: interrogate
description: "Trigger: interrogate, /interrogate, adversarial review, stress test diff, judgment day. Read-only breaking probes where only runtime-proven failures survive."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "2"
disable-model-invocation: true
---

## Activation Contract

Load only when the user invokes `/interrogate` or asks for an adversarial review of a diff or design.

## Hard Rules

- A finding survives only when a command, failing test, or repro script run in an isolated `mktemp -d` copy proves it. Drop style notes, guesses, and risks that need a future change.
- Adversaries never modify the main workspace and report their scratch paths.
- Default to 1 read-only `pig-verifier` on `inherit-parent`. Use 2 blind adversaries only when the user asks for dual review or `.pig-stack/models.md` sets `interrogate reviewers`.
- Report only. Fixing findings is a separate request that follows the ODD correction bounds.

## Decision Gates

| Request | Topology |
|---|---|
| Default | 1 `pig-verifier` deriving boundary, negative, and differential probes. |
| Dual review requested or configured | 2 blind adversaries; keep only findings the parent reproduces. |
| Design with no code | Probe the current tree; mark unrun claims `UNPROVEN`. |

## Execution Steps

1. Lock the scope (branch diff from merge-base plus working tree, or named files) and state the intent with `in-your-own-words`.
2. Spawn the adversary with intent, baseline ref, scope, and skill paths.
3. Re-run each reported command in the parent. Keep failures that break the intent, merge shared root causes, drop the rest.
4. Remove reported scratch paths.

## Output Contract

Return: intent, verified findings (command, output, broken intent), dropped count with reasons, cleanup confirmation.
