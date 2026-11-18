# Playbook: Investigation

**Goal:** Answer how or why a system works, or compare alternatives, strictly read-only.

1. **Enforce read-only:** Never edit source files, create tasks, or spawn implementation writers (`Authorize` step 1).
2. **Explore proportionately:** Use one bounded read batch when narrow. Spawn one read-only `pig-explorer` only when the Mapping trigger holds.
3. **Ground in record:** Use `how` for runtime mechanics and `why` for commit/PR rationale. Cite exact `path:line` or commit SHAs, and separate observed facts from inferences.
4. **Push back when warranted:** If the premise is flawed or an alternative is simpler, state your direct judgment with a concise tradeoffs table.
5. **Unslop:** Apply `unslop` to the final answer.

**Reply:** Overview, Mechanism (`path:line`), Tradeoffs/Verdict (if deciding), and Open Unknowns.
