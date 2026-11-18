---
name: no-comments
description: "Trigger: no-comments, /no-comments, strip comments, comment ban. Audits comments with read-only comment-sicko, deletes banned ones, and fixes trivial root causes."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "1"
---

## Activation Contract

Load when called by `deslop`, or when the user invokes `/no-comments`.

## Hard Rules

- `comment-sicko` owns the exception list and audits read-only. One audit per pass. Never re-spawn it on the same scope.
- Never shorten a workaround comment into a smaller one. Delete it, and fix or report the root cause.
- Fix a `MUST KILL` inline only when it is trivial and inside the scope (dead path, unused parameter, wrong API, rename). Report every other `MUST KILL` as an open item. Never start a design step from here.
- Replace a `do not remove` claim with a type, assertion, or test only when that change is inside the scope. Otherwise delete the comment and report the unenforced constraint.
- Deleting comments alone needs only a syntax or typecheck run. Behavior checks run only after a `MUST KILL` code fix.

## Decision Gates

| Finding | Action |
|---|---|
| `DELETE` | Delete the lines in one edit pass. |
| `KEEP` | Leave untouched. |
| `MUST KILL`, trivial and in scope | Fix inline, delete the comment. |
| `MUST KILL`, needs a design change | Delete the comment, report the symbol and the proposed fix as open. |
| `KEEP` claim looks doubtful | Check it once with `why`. If still unproven, delete. |

## Execution Steps

1. Take the file list from the caller, or `git diff <base>...HEAD` plus the working tree.
2. Spawn read-only `comment-sicko` once with that list.
3. Apply every `DELETE` and every trivial `MUST KILL` in one pass.
4. Run the syntax or typecheck command once. When a `MUST KILL` changed code and the call is standalone, also run the focused tests once.

## Output Contract

Return: `DELETE` count, `KEEP` count with exception numbers, `MUST KILL` fixed inline, `MUST KILL` reported open, and check output.
