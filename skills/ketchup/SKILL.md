---
name: ketchup
description: "Trigger: ketchup, /ketchup, catch up, what changed in this chat. Summarizes session progress since the user's last message and lists every pending human call."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "6"
---

## Activation Contract

Load when the user invokes `/ketchup` to catch up on session changes and open human decisions.

## Hard Rules

- **Read-only summary:** Never edit code, start jobs, or run mutating actions during `/ketchup`.
- **Plain words (`bro` voice):** Explain what changed for the user, not low-level mechanics, omitting hashes/paths unless required to decide an action item.
- **Self-contained action items:** List every pending human call (product choice, approval, irreversible step) with your recommended pick, supporting evidence, and risk so the user can decide from the reply alone.
- **Truth check:** Never mark items still waiting on the user as done; verify claimed PR/test states from session outputs.

## Decision Gates

| Pending Human Calls | Format |
|---|---|
| Zero calls waiting | State "Nothing is waiting on you" + concise summary of changes. |
| One or more calls waiting | Lead with count of calls, short summary (< 100 words), then each call with pick + evidence + risk. |

## Execution Steps

1. Gather all changes, subagent results, and PR/test outcomes since the user's last message.
2. Separate completed work from items blocked on a human decision or still running.
3. Draft concise summary + small Mermaid visual only if a flow/dependency needs it (<= 6 boxes).

## Output Contract

Return: opening status line, brief summary of changes, optional small visual, and self-contained list of calls waiting on the user.
