---
name: unslop
description: "Trigger: unslop, /unslop, clean writing, remove AI tells. Rewrites prose, docs, and replies to remove AI patterns while keeping facts exact."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "0"
---

## Activation Contract

Load when cleaning prose, documentation, PR text, or chat replies, or when the user invokes `/unslop`. Never apply to code comments.

## Hard Rules

Apply every rule and keep every fact, qualifier, and number:

1. Cut trailing `-ing` filler clauses ("highlighting...", "ensuring...").
2. Name the source of a claim or delete the attribution ("experts believe").
3. Ban: `additionally`, `crucial`, `delve`, `enhance`, `foster`, `landscape`, `pivotal`, `showcase`, `testament`, `underscore`, `vibrant`, `leverage`, `utilize`.
4. Say `is` or `has`, never `serves as`, `stands as`, `boasts`, `features`.
5. Cut "not just X, but Y" and forced groups of three.
6. One name per thing. Repeat it.
7. No em dashes, en dashes, or dash-hyphens. No colon as a mid-sentence connector.
8. No bold label that restates its line, no decorative emojis, no bolding every noun.
9. No chatbot openers or closers. "In order to" becomes "to".
10. Ban abstract metaphor nouns (`substrate`, `wedge`, `vector`, `nexus`, `primitive`, `harness`, `surface`, `scaffolding`, `paradigm`, `ratchet`, `north star`, `flywheel`) when a concrete word exists. Keep established concrete technical terms (`test harness`, `API surface`) only when naming that specific artifact.
11. One idea per sentence, active voice, numbers over adverbs.

## Decision Gates

| Text | Handling |
|---|---|
| Chat reply | Apply rules 1-11 before sending. |
| Docs or PR text | Apply rules 1-11 once. |
| A rule makes a sentence wrong or unclear | Keep the clear sentence. Accuracy wins. |

## Execution Steps

1. Scan the text against rules 1-11.
2. Replace filler and metaphors with the concrete mechanism, path, or number.
3. Confirm no fact or qualifier was lost.

## Output Contract

Return the cleaned text, or a diff summary when editing files.
