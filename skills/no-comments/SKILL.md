---
name: no-comments
description: "Trigger: no-comments, /no-comments, strip comments, comment ban. Audits comments inline for small diffs or with comment-sicko for large diffs, deletes banned ones, and fixes trivial root causes."
license: MIT
metadata:
  author: pig-stack
  version: "1.2"
  layer: "1"
---

## Activation Contract

Load when called by `deslop`, or when the user invokes `/no-comments`.

## Hard Rules

- `agents/comment-sicko.md` defines the canonical exception list. Audit each scope once and never re-spawn `comment-sicko` on the same scope.
- Small diffs (`<= 3` files and `<= 100` changed lines) run inline with no subagent, applying the same exception list directly. Spawn read-only `comment-sicko` only when the diff exceeds that threshold or on a broad standalone `/no-comments` audit.
- Never shorten a workaround comment into a smaller one. Delete it, and fix or report the root cause.
- Fix a `MUST KILL` inline only when it is trivial and inside the scope (dead path, unused parameter, wrong API, rename). Report every other `MUST KILL` as an open item. Never start a design step from here.
- Replace a `do not remove` claim with a type, assertion, or test only when that change is inside the scope. Otherwise delete the comment and report the unenforced constraint.
- Deleting comments alone needs only a syntax or typecheck run. Behavior checks run only after a `MUST KILL` code fix.

## Decision Gates

| Condition / Finding | Action |
|---|---|
| Small diff (`<= 3` files and `<= 100` changed lines) | Audit inline against `agents/comment-sicko.md` exceptions; no subagent. |
| Larger diff (`> 3` files or `> 100` changed lines) | Spawn read-only `comment-sicko` once with the locked file list. |
| `DELETE` | Delete the lines in one edit pass. |
| `KEEP` | Leave untouched. |
| `MUST KILL`, trivial and in scope | Fix inline, delete the comment. |
| `MUST KILL`, needs a design change | Delete the comment, report the symbol and the proposed fix as open. |
| `KEEP` claim looks doubtful | Check it once with `why`. If still unproven, delete. |

## Execution Steps

1. Take the file list from the caller, or resolve `<base>` (`git merge-base HEAD origin/HEAD`, fallback local `main`/`master`, else working tree) and collect changed files.
2. Audit inline for small diffs, or spawn read-only `comment-sicko` once for larger diffs.
3. Apply every `DELETE` and every trivial `MUST KILL` in one pass.
4. Run the syntax or typecheck command once. When a `MUST KILL` changed code and the call is standalone, also run the focused tests once.

## Output Contract

Return: audit route (`inline` or `comment-sicko`), `DELETE` count, `KEEP` count with exception numbers, `MUST KILL` fixed inline, `MUST KILL` reported open, and check output.
