---
name: pig-help
description: "Trigger: pig-help, /pig-help, which skill, how to use pig-stack. Guides setup, ODD workflow, and skill selection without starting paid work."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "5"
---

## Activation Contract

Load when the user asks how `pig-stack` works, which skill to use, or how to configure budgets and runtimes.

## Hard Rules

- **Read-only guidance:** Never start implementation or spawn coding subagents for a help question. Give the answer and a copy-paste prompt.
- **Verify state before recommending:** Check whether `.pig-stack/models.md`, `.atl/skill-registry.md`, or a `verify-*` skill exists in the active workspace before suggesting setup steps.
- **Redirect work requests:** If the user asks to actually fix or build something ("use pig-stack to fix X"), load `pig-mode` and run the task instead.

## Decision Gates

| User Need | Route / Recommendation |
|---|---|
| General feature, bug, refactor, or investigation | `/pig-mode` (ODD handles sizing and delegation automatically) |
| Configure $20 budget / role models | `/setup-pig-stack` |
| Clean AI code + comment slop before PR | `/deslop` (runs `no-comments` once) |
| Design types/boundaries before coding | `/architect` |
| Parallel disjoint slices | `/pig-swarm` (opt-in) |
| Adversarial check / design bakeoff | `/interrogate` or `/arena` (opt-in) |
| Prove real app behavior end-to-end | `/create-verification-skill` |

## Execution Steps

1. Inspect workspace state (`.pig-stack/models.md`, `.atl/skill-registry.md`, `odd/tasks/`).
2. Answer the user's question directly using `unslop` style.
3. Provide at most one ready-to-send prompt example matching their need.

## Output Contract

Return: concise answer, relevant workspace status note (only if actionable), and one example prompt.
