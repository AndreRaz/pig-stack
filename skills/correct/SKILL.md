---
name: correct
description: "Trigger: correct, /correct, repeated mistake, enforce rule. Makes a recurring agent mistake impossible via architecture, types, lint, or tests."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "3"
disable-model-invocation: true
---

## Activation Contract

Load when the user points out a mistake agents repeat in this repository, or invokes `/correct`.

## Hard Rules

- A class counts only after it happened at least twice.
- Use the highest level that blocks it: architecture, then types or schemas, then a lint or CI check whose error names the fix, then a behavior test, then a written rule last.
- Prove each new check fails on a real past mistake or a minimal reproduction before keeping it.
- Every written rule in `AGENTS.md` names what enforces it. Remove a rule once its mistake cannot happen.

## Decision Gates

| Mistake | Level |
|---|---|
| Agents use an old API or wrong helper | Delete the old API, hide internal exports. |
| Invalid value combinations | Type that makes them unrepresentable. |
| Bad pattern still compiles | Lint or CI script naming the right API. |
| Behavior regression | Behavior test. |

## Execution Steps

1. Group mistakes from recent commits, reverts, and user corrections.
2. Pick the highest working level for each class.
3. Implement it, prove it fails on the mistake, then run the Close Sequence once (`deslop`, verification).
4. Update the rule-to-enforcer table in `AGENTS.md` when one exists.

## Output Contract

Return: each class with evidence, the chosen level and why higher levels failed, proof the check fails on the mistake, and verification output.
