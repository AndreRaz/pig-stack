---
name: sharpen
description: "Trigger: sharpen, /sharpen, improve this prompt. Rewrites a prompt to be deeper and verifiable without executing the task."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "6"
disable-model-invocation: true
---

## Activation Contract

Load only when the user invokes `/sharpen` or asks to strengthen a prompt before sending it.

## Hard Rules

- Rewrite only. Never run the task, edit files, or spawn workers.
- Add what a senior engineer would insist on: the primary files or data, a falsifiable check, prototype-first for empirical forks, and explicit non-goals.
- Leave product and preference choices to the user as one-line blanks.
- Keep the rewrite shorter than twice the original.

## Decision Gates

| Draft | Add |
|---|---|
| Bug or performance | Baseline repro or measurement, root-cause evidence, differential check. |
| Feature or design | Data shape first, boundary invariants, concrete proof predicate. |

## Execution Steps

1. Read the draft and, when paths are mentioned, confirm they exist.
2. List the missing inputs, hidden assumptions, and the outside check.
3. Rewrite as a `pig-mode` prompt and run `unslop` on it.

## Output Contract

Return the prompt in one code block, then at most three bullets on what was added and any open choice.
