---
name: tdd
description: "Trigger: tdd, /tdd, test-first, failing test, regression test. Drives RED-GREEN-REFACTOR with preservation tests on shared code."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "0"
---

## Activation Contract

Load when a behavior change or bug fix has a cheap deterministic test path, or when the user invokes `/tdd`.

## Hard Rules

- Observe RED before writing production code. A test file existing is not RED.
- RED must fail for the intended reason. A test that fails on an import error or a typo is not RED; fix the test first.
- Assert observable behavior: outputs, exit codes, persisted state. Never assert private internals or mock call counts.
- Write one test per requested rule, plus one preservation test per existing command or option that shares the changed code. Add no other cases.
- Prefer no new test over a brittle one. When the only path needs heavy mocks or slow infrastructure, record the exception and use the closest real executable check.
- Never weaken an existing assertion to make a change pass.

## Decision Gates

| Situation | Action |
|---|---|
| Deterministic local test path | RED, then smallest fix, then GREEN, then refactor with tests green. |
| Only brittle or mock-heavy test path | Record the exception, run a real repro command instead. |
| Passive docs or config with no behavior | Skip. Structural readback only. |

## Execution Steps

1. Name the expected behavior, the boundary inputs, and the test runner.
2. Add the focused tests and the preservation tests.
3. Run them and capture the RED output.
4. Implement the smallest change, run the same tests, capture GREEN.
5. Refactor while those tests stay green. The full suite runs later in the Close Sequence.

## Output Contract

Return: test command, observed RED output, observed GREEN output, or the stated exception with the substitute check.
