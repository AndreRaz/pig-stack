# Playbook: Refactoring

**Goal:** Lower reader load while observable behavior stays identical.

1. **Pin behavior:** Confirm existing tests cover the area, or add a characterization check first. Typecheck and lint are not a pin.
2. **Subtract first:** Delete dead code, orphan branches, redundant internal guards, and one-caller wrappers.
3. **Target shape:** Run `architect` once only when a cross-module type or state owner changes. Never add indirection that removes no branch or invalid state.
4. **Migrate in one wave:** Move every caller and delete the old API together. Keep a compatibility shim only for an external contract (`Risk: item 3`).
5. **Close:** Close Sequence once, plus an equivalence check against the baseline. If reader load did not drop, revert.

**Reply:** structure changed, behavior pin, equivalence proof, reader-load delta, `Risk:` line.
