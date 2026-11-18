---
name: in-your-own-words
description: "Trigger: in-your-own-words, /in-your-own-words, restate the goal. Plays back problem, constraints, and non-goals before starting work."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "1"
---

## Activation Contract

Load when the user asks you to restate their goal/problem before acting, or when verifying understanding of a dense issue thread.

## Hard Rules

- **Read-only playback:** Do not edit files, create plans, or launch writers.
- **No leading assumptions:** State the underlying problem, desired outcome, hard constraints, and explicit non-goals in plain words without echoing vague phrasing verbatim.
- **Wait when clarifying:** If a critical ambiguity or premise mismatch surfaces, ask one focused question and wait.

## Decision Gates

| Ambiguity Found | Action |
|---|---|
| Interpretation is clear and complete | Present restatement and ask user to confirm or redirect. |
| Critical contradiction or missing constraint | Present restatement + 1 focused question, then stop. |

## Execution Steps

1. Read the user's message and referenced thread/files minimally.
2. Extract: Goal, Current Symptom/State, Constraints, Non-Goals, and Success Check.
3. Apply `unslop` and present concisely.

## Output Contract

Return: Goal, Problem/Context, Constraints, Non-Goals, Falsifiable Success Check, and any single open question.
