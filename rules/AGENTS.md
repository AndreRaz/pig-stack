# pig-stack Core Rules

Organic Driven Development (ODD) is the default workflow. Full detail lives in `skills/pig-mode/references/odd-protocol.md`; load it only for large or high-risk work.

## Workflow

- Authorize first: explain, review, audit, compare, and plan requests stay read-only.
- Small tasks (understood, no High-Risk item, resumable from the request plus `git diff`) run inline with no feature document and no subagents.
- Large tasks create `odd/tasks/<feature-name>.md` before the first source write.
- Delegate only on a real trigger (exact rules in `odd-protocol.md` section 3): Mapping, Writer (2+ independent ~100-line units with disjoint edit paths), or Verification (High-Risk: data, security, shared contracts, concurrency, delivery, no regression test).
- Close once: `deslop`, then verification, then `pig-verifier` only for High-Risk. One correction batch plus one recheck (two max if the same blocker persists or the correction introduced a regression). Never loop.

## Budget

- All subagents use `inherit-parent` unless `.pig-stack/models.md` overrides a role.
- `arena`, `interrogate` panels, and `pig-swarm` run only when the user asks.

## Code

- No comments except license headers, public API doc contracts, functional directives (build tags, type-checker or linter pragmas, shebangs), verifiable external constraints, and short sourced domain/algorithm/regex notes.
- No dead code, one-caller wrappers, speculative fallbacks, or duplicated helpers. Parse external data at boundaries.
- Commit only when asked or for tracked large-task work units on a feature branch.

## Reporting

- Report `<command>: <observed result>`. A build or a subagent self-report is not proof.
- Short declarative sentences. No filler.
