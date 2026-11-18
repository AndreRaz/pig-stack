---
name: bro
description: "Trigger: bro, /bro, explain in plain words, no jargon. Restates the last reply or dense technical answer in short, plain human language."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "1"
---

## Activation Contract

Load when the user invokes `/bro` or asks for the previous message in plain, jargon-free language.

## Hard Rules

- **Read-only restatement:** Never run tools or mutate files unless a factual check is missing.
- **Zero jargon:** Replace internal abstractions, file paths, and hashes with what actually broke, changed, or needs a decision for a human reader.
- **Shorter than the original:** Cut filler; preserve every concrete risk, number, and open decision accurately.

## Decision Gates

| Last Reply Had | Focus |
|---|---|
| Technical fix/feature | What changed for the user, whether it is verified, and any risk. |
| Pending decision/blocker | Plain explanation of the choice and what happens with each option. |

## Execution Steps

1. Extract the core outcome, evidence status, and any decision waiting on the user from the last reply.
2. Rewrite in short, conversational sentences with no jargon.

## Output Contract

Return only the plain-language restatement.
