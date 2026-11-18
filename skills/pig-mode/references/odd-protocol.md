# ODD Protocol Reference

Single source of truth for ODD steps, delegation triggers, the close sequence, correction bounds, and commit policy. Other files reference this one instead of restating it.

## 1. Seven-Step Protocol

1. **Authorize:** Read-only requests (`explain`, `review`, `audit`, `compare`, `plan`) never mutate code or spawn writers. Clarify ambiguous change intent once and stop.
2. **Explore:** Gather the evidence needed to decide, in one parallel batch of at most 3 bounded reads (~10k tokens). Reading the files you are about to edit belongs to the edit and never counts against this budget.
3. **Resolve uncertainty:** Settle technical forks by running code or a small prototype. Ask one focused question only for a genuine product decision or ambiguous authorization, then wait.
4. **Classify (Resume Test):**
   - **Small:** Outcome understood, no High-Risk item, and resumable from the request plus `git diff` alone. Work inline. No feature document. File, line, or test counts never decide size.
   - **Large:** Fails the Resume Test (multi-session, external waits, separable deliverables, or specs too long to survive compaction).
5. **Track (large only):** Create `odd/tasks/<feature-name>.md` before the first source write, without asking:
   ```markdown
   # Feature: <name>
   Branch: <branch> | Runner: <test command>

   ## Specs
   - S1: "<verbatim user rule, string, error message, or example>"

   ## Tasks
   - [ ] T1 (S1) | Route: inline | Commit: pending

   ## Log
   - L1: "<verbatim original user request>"
   ```
   A requirement change appends a verbatim `## Log` entry, rewrites only the affected `S#`, and reopens only linked tasks.
6. **Implement task by task:** Hand off by reference (`Spec: odd/tasks/<feature>.md, T2, S3-S4`), never by paraphrase. Apply `RED -> GREEN -> REFACTOR` when a deterministic test path exists.
7. **Close:** Run the Close Sequence (section 4) once.

## 2. High-Risk List

Only a named item triggers `pig-verifier`:

1. **Data:** Migrations or altering persisted data that cannot be rebuilt.
2. **Security:** Auth, permissions, credentials, secrets, sandbox boundaries.
3. **Shared contracts:** Changing public APIs, CLI flags, config formats, exports, or helpers used by behavior the request did not mention.
4. **Concurrency:** Locks, races, async ordering.
5. **Delivery:** Installers, CI, release, deploy, dependencies.
6. **No regression test:** A behavior change no automated test would catch.

## 3. Delegation Triggers

No trigger holds by default. When in doubt, work inline.

- **Mapping:** Understanding needs more than one bounded read batch (3 parallel reads, ~10k tokens) or more than ~5 sequential lookups before you can decide. Spawn one read-only `pig-explorer` (handoff <= ~2k tokens, one parent spot check).
- **Writer:** Two or more independent behavior units (~100+ changed lines each) with disjoint `## Allowed edit paths`, launched in the same turn, or the ~150k parent-context backstop. Size or file count alone never qualifies.
- **Verification:** The `Risk:` line names an item from section 2. Spawn one read-only `pig-verifier`.
- **Parallel writers:** Same local tree only with disjoint edit paths, the parent owns git, workers run no repo-wide formatters or installs. Use isolated worktrees only when units share a file.

## 4. Close Sequence (run once, in order)

1. **Normalize:** Run `deslop` once over the diff. It runs `no-comments` internally (inline for small diffs, `comment-sicko` only for large diffs). Never call `no-comments` separately in the same pass.
2. **Verify:** Run focused checks, then the applicable full suite, then a differential check on touched shared helpers. This is the only full verification run.
3. **Independent check:** Spawn `pig-verifier` only when section 2 applies.
4. **Report:** Observed `<command>: <result>`, `Risk: item N (reason)` or `Risk: none`, and every skipped or unverified check.

## 5. Correction Bounds

- A failed check or verifier blocker gets one correction batch fixing every reported blocker, then one recheck limited to those blockers.
- The correction diff gets `deslop` scoped to the changed lines only, never a new full normalization pass.
- A second (and final) correction runs only when the recheck shows the same blocker still failing, or a regression introduced by the correction diff itself. Pre-existing or out-of-scope new findings never earn another round.
- Still failing after the second correction (or if a correction-caused regression remains unresolved): apply `Attack the Premise` once. If no new hypothesis exists, stop and report the unit as `partial` with the exact blocker.

## 6. Commit Policy

- Commit only when the user asks, or for work-unit commits of a large tracked task on a feature branch.
- Never commit on the default branch without explicit instruction. Push, PR creation, and merge always need explicit user authorization.
- Use Conventional Commits (`type(scope): subject`), no AI attribution. Isolate High-Risk units in their own commit.
