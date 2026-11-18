# Playbook: Feature

**Goal:** New or changed behavior with a clean data shape and real verification.

1. **Explore:** Confirm change intent. Gather decision evidence in one bounded batch, or one `pig-explorer` when the Mapping trigger holds.
2. **Shape:** When a cross-module type, signature, or state owner changes, run `architect` once. Otherwise name the data shape in one line and continue.
3. **Classify:** Resume Test. Large tasks get `odd/tasks/<feature>.md`.
4. **Implement:** Inline by default. Use `pig-worker` only when the Writer trigger holds. Use `tdd` when a deterministic test path exists.
5. **Close:** Close Sequence once (`deslop`, verification, `pig-verifier` only for High-Risk). Commits follow odd-protocol section 6.

**Reply:** goal, chosen shape, observed verification, `Risk:` line, open items.
