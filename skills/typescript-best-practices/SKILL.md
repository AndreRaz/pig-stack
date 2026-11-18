---
name: typescript-best-practices
description: "Trigger: typescript-best-practices, .ts, .tsx, TypeScript types. Enforces boundary parsing, discriminated unions, branded types, and exhaustiveness."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "0"
paths: ["**/*.ts", "**/*.tsx"]
---

## Activation Contract

Load when designing, editing, or reviewing `.ts` or `.tsx` code.

## Hard Rules

- Parse external data (`unknown`, JSON, API, CLI, env) once at the boundary with the repository's schema library. Never let `any` or `Record<string, unknown>` cross into domain code.
- Model variants as discriminated unions with a literal `kind`, not optional-property bags.
- No `as` on unvalidated data. Prefer `satisfies`, narrowing, or a type guard that really checks.
- End union switches with `const _exhaustive: never = value;`.
- Derive types (`z.infer`, `Pick`, `Omit`, `ReturnType`, `typeof`) before declaring a parallel interface.
- Mock only what cannot run locally. Use a structured logger instead of `console.log` in shipped code.
- Follow the repository's existing schema library and strictness. Never introduce a new one for a local change.

## Decision Gates

| Anti-pattern | Replacement |
|---|---|
| `x as T` on external input | Schema `.parse()` or a checking `isT(x)` guard. |
| Synced booleans (`isLoading`, `isError`) | `{ status: "loading" } \| { status: "error"; error: E }`. |
| Duplicated interface | Derived type. |

## Execution Steps

1. Read `tsconfig` strictness and the existing schema and domain types.
2. Apply the rules above to the touched code only.
3. Run the repository typecheck once (for example `tsc --noEmit`).

## Output Contract

Return: invariants applied, files edited, typecheck output.
