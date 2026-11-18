# Engineering Principles Index

Read the specific entry that guides a decision and cite only principles that actually changed your design or code in this session.

## Core

- **Laziness Protocol:** Bias toward deletion and the smallest change that solves the problem. Consolidate repeated decisions behind one source of truth.
- **Foundational Thinking:** Settle core types, data structures, scaffold-vs-feature order, and shared concurrent state before writing logic.
- **Redesign from First Principles:** When integrating a new requirement, reshape as if it had been foundational from day one instead of bolting on patches.
- **Attack the Premise:** When two fixes sharing one premise fail the same gate, stop, write the premise down, and test it directly before coding a third fix.
- **Subtract Before You Add:** Delete dead code, redundant validators, and stub references first, then build on the simpler base.
- **Minimize Reader Load:** Count layers between question and answer and hidden mutable state; collapse 1-caller wrappers and shrink scope.
- **Outcome-Oriented Execution:** In planned migrations/rewrites, converge on the target architecture instead of maintaining throwaway compatibility shims.
- **Experience First:** Choose user clarity and polish over implementation convenience; ship fewer solid features over more rough ones.
- **Exhaust the Design Space:** For high-cost novel designs with no precedent, prototype 2-3 competing options side by side (`arena` or `prototype`) before committing.
- **Build the Lever:** For repeated edits, migrations, or checks, write a deterministic script/codemod/check reviewers can rerun instead of manual edits.

## Architecture

- **Model the Domain:** Encode stateful or branching logic in a state machine, discriminated union, table, or registry instead of scattered `if/else` flags.
- **Boundary Discipline:** Validate and parse external data at system boundaries (CLI, config, network, APIs); trust internal domain types and keep core logic pure.
- **Type System Discipline:** Make illegal states unrepresentable, brand semantic primitives, parse external data with schemas, and exhaust variants.
- **Make Operations Idempotent:** Design commands, installers, and lifecycle steps so retries converge to the same clean end state.
- **Migrate Callers Then Delete Legacy APIs:** Migrate all callers and remove the old API in the same wave instead of preserving dual paths.
- **Separate Before Serializing Shared State:** Eliminate shared mutable targets first (disjoint edit surfaces); serialize structurally only when one writer is a true invariant.

## Verification

- **Prove It Works:** Verify against the real artifact (executed command, real UI/CLI output, diff), never a proxy like "it compiles" or a self-report.
- **Fix Root Causes:** Trace each symptom back to the first point of failure and fix it there; add a guard only for legitimate boundary states.
- **Sequence Verifiable Units:** Break multi-step work into small verifiable units; check each unit before starting the next and stack clean commits.
- **Test Behavior, Not Implementation:** Assert observable inputs, outputs, exit codes, and persisted state so refactors do not break valid tests.
- **Explain the Number:** Before trusting or reporting a benchmark, identify the limiter, rule out measurement bugs, and verify repeat runs (`benchmark-checklist`).

## Delegation

- **Guard the Context Window:** Keep main thread thin; offload maps that need more than one bounded read batch to `pig-explorer` and keep raw payloads out of the orchestrator.
- **Never Block on the Human (on Reversible Work):** Proceed on reversible technical choices and disclose them; stop ONLY for ambiguous authorization, unresolved product decisions, or destructive/publishing actions.

## Meta

- **Encode Lessons in Structure:** Whenever you repeat a prose rule twice, encode it as a type, schema, lint check, or test instead of adding more prompt text.
