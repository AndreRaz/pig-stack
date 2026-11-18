---
name: deslop
description: "Trigger: deslop, /deslop, clean slop, anti-slop, tighten diff. Strips AI code slop and banned comments from a diff in one normalization pass."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "2"
---

## Activation Contract

Load as step 1 of the ODD Close Sequence, or when the user invokes `/deslop`.

## Hard Rules

- Scope is the diff against the base branch (default `main`) plus the working tree, unless the user names paths.
- Behavior stays identical. Removing slop never drops real validation.
- Keep error handling at system boundaries: I/O, network, parsing, user input, process exit codes. Delete a guard only when a type or an upstream boundary already guarantees the invariant.
- Run `no-comments` exactly once per pass, from here. Callers never run it separately.
- Extract a shared helper only for identical logic with the same reason to change. Two similar blocks with different reasons stay separate.
- One pass only. Never re-run `deslop` on its own output.

## Decision Gates

| Pattern | Action |
|---|---|
| One-caller wrapper or pass-through abstraction | Inline it and delete the wrapper. |
| Dead imports, unused variables, unreachable branches, orphan shims | Delete. |
| Internal guard duplicated by a type or upstream boundary | Delete the inner guard. |
| `any`, unsafe cast, or unparsed external data | Parse once at the boundary into a domain type. |
| Comments of any kind | Leave for `no-comments` in step 3. |
| Prose in docs or PR text | `unslop`. |

## Execution Steps

1. Lock the file list from `git diff <base>...HEAD` and `git diff`.
2. Remove each slop pattern at its root without widening scope.
3. Run `no-comments` once over the same file list.
4. Run `unslop` on edited docs and PR text.
5. Inside the Close Sequence, stop here: verification runs next. When invoked standalone, run the focused checks once.

## Output Contract

Return: files cleaned, slop categories removed with counts, the `no-comments` summary, and focused check output when run standalone.
