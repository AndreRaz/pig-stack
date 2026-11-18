---
name: how
description: "Trigger: how does X work, /how, subsystem walkthrough, where should this live. Maps runtime flow, ownership, and layering strictly read-only."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "1"
---

## Activation Contract

Load when the user asks how a subsystem works, where new logic belongs, or which layer owns a piece of state.

## Hard Rules

- **Strictly read-only:** Never edit files or spawn writers.
- **Proportionate reading:** Use 1 inline parallel batch (<= 3 calls, ~10k tokens) for narrow subsystems; spawn 1 read-only `pig-explorer` only when understanding needs more than one batch or ~5 sequential lookups.
- **Cite observed code:** Every claim about runtime behavior, types, or ownership must cite `path:line`. Mark inferences explicitly.

## Decision Gates

| Scope | Route |
|---|---|
| <= 3 bounded reads suffice | Explore inline directly. |
| Trace needs more than one batch | Spawn 1 `pig-explorer` with `Skills to load before work`. |
| User asked "why was it built this way?" | Route to or pair with `why`. |

## Execution Steps

1. State the scoped interpretation if ambiguous without blocking.
2. Trace entry points, core data shapes, state owners, and boundary adapters.
3. Synthesize a concise architectural walkthrough using `unslop` rules.

## Output Contract

Return: Overview, Key Data Shapes & Owners, Runtime Flow (`path:line`), Layering/Placement note (if asked), and Gotchas/Unknowns.
