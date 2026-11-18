---
name: blast-radius
description: "Trigger: blast-radius, /blast-radius, what could this break, safety check. Finds non-obvious downstream breakage and proves safety by running code."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "2"
---

## Activation Contract

Load when auditing a change for hidden cross-module, schema, serialization, lifecycle, or contract breakage before merge.

## Hard Rules

- **Beyond grep:** Do not stop at direct symbol callers. Inspect wire formats, JSON/DB schemas, shared helpers, async teardown order, feature flags, and downstream library code.
- **Proof by execution beats prose:** Every critical safety claim ("this cannot break X") must be tested by running a real script, test, or isolated command whenever feasible (`Prove It Works`).
- **Evidence ladder:** Explicitly grade each safety invariant: `(1) asserted` < `(2) cited file:line` < `(3) traced path` < `(4) executed script/test` < `(5) live app repro`.
- **Clean up scratch:** Run ad-hoc repros in `mktemp -d` and remove scratch files afterward.

## Decision Gates

| Change Scope | Route |
|---|---|
| Small diff or single boundary | Execute inline + isolated `mktemp` verification script. |
| Wide cross-cutting change | Spawn 1 `pig-explorer` for downstream consumers, then prove critical invariants with executed code. |

## Execution Steps

1. Read the diff and identify every changed contract, shared helper, or side effect.
2. State the 1-2 core facts the change's safety depends on.
3. Trace hidden consumers beyond symbol grep (`file:line`).
4. Run a targeted script or test against the real code to prove each safety fact (or mark `UNPROVEN`).

## Output Contract

Return: what changed, core safety invariant(s) with evidence ladder level + pasted command output, confirmed risks (`file:line`), cleared checks, and recommended regression test.
