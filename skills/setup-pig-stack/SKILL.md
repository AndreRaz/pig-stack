---
name: setup-pig-stack
description: "Trigger: setup-pig-stack, /setup-pig-stack, configure models, pig-stack budget. Configures $20-friendly model budgets and optional project verification."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "5"
---

## Activation Contract

Load when initializing `pig-stack` in a workspace, configuring role models, or tuning token budget (`$20` tier vs custom multi-model).

## Hard Rules

- **Safe $20 default:** Default all roles to `inherit-parent` (`balanced`) so subagents use the active subscription model without burning extra quota on expensive panels.
- **No invented model slugs:** Only write `inherit-parent`, `auto`, or model identifiers confirmed available in the active runtime.
- **Idempotent config:** Write `.pig-stack/models.md` in the workspace (or the runtime's user rule path per `docs/runtimes/multi-runtime.md`) so re-runs overwrite cleanly without duplicating rules.
- **Ask at most one focused step at a time:** Confirm budget tier before writing.

## Decision Gates

| Budget Tier | Default Role Mapping | Best For |
|---|---|---|
| `balanced` (Recommended, $20 tier) | All roles `inherit-parent`; panels opt-in only | Claude Pro / Codex / Antigravity daily work |
| `economy` | `pig-explorer` and `comment-sicko` on fastest/lightest tier; workers `inherit-parent` | Long exploration and heavy diffs on tight quota |
| `multi-model` | Explicit per-role slugs for `worker`, `verifier`, opt-in `arena`, and opt-in `interrogate` | Multi-vendor adversarial checks when budget permits |

## Execution Steps

1. Inspect existing `.pig-stack/models.md` (and runtime model rules if present) plus available runtime model choices.
2. Ask the user to select a budget tier (`balanced`, `economy`, or `multi-model` with explicit role overrides).
3. Write the idempotent configuration file (`.pig-stack/models.md` plus `.atl/skill-registry.md` refresh via `python3 scripts/generate_registry.py` if in repo, or `skill-registry`).
4. Offer once to generate a project verification skill (`create-verification-skill`) if no `verify-*` skill exists yet.

## Output Contract

Return: config file path written, selected budget tier and role mapping, skill-registry status, and whether verification skill setup was requested.
