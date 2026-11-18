# Playbook: Prototype

**Goal:** Settle an empirical or design fork cheaply with runnable code before committing to production implementation.

1. **Name the question:** State the exact fork or assumption being tested (`Experience First` / `Exhaust the Design Space`).
2. **Keep throwaway isolated:** Build the minimal prototype in `/tmp` or a temporary branch/directory so it never pollutes production code.
3. **Compare side by side:** If comparing 2 options, evaluate both on the same concrete criteria and observable behavior (suggest `/arena` as opt-in only if parallel isolated candidates are explicitly warranted).
4. **Decide & Discard:** Record the chosen direction and delete throwaway prototype artifacts before implementing the real solution cleanly.

**Reply:** fork tested, observed evidence from running the prototype, chosen option, and cleanup status.
