---
name: create-verification-skill
description: "Trigger: create-verification-skill, /create-verification-skill, verify skill, control skill. Generates and proves a project-local verify-<app> skill."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "3"
---

## Activation Contract

Load when a project lacks a scripted way to launch, drive, and verify the real running app from a user perspective.

## Hard Rules

- **Interview the repo first:** Derive surface, start command, harness, evidence path, and isolation rules from code/scripts; ask the user only what is unobservable.
- **No unproved draft:** Run the generated skill end-to-end once (launch -> doctor -> drive 1 feature -> capture evidence -> cleanup) before handing it back.
- **Preserve evidence across cleanup:** Cleanup kills only processes/temp state it started and leaves proof artifacts intact at the named path.
- **Portable target path:** Write to `.agents/skills/verify-<app>/` (or `.cursor/skills/verify-<app>/` when Cursor-only).

## Decision Gates

| App Surface | Default Harness |
|---|---|
| Web / Electron UI | Playwright / browser tool / CDP using ARIA/test-id selectors |
| CLI / TUI | Isolated PTY / `tmux` session per drive |
| Service / API | Local server + HTTP/CLI client against isolated data dir/DB |

## Execution Steps

1. Inspect package scripts, Makefile, README, and existing test harnesses to map Launch, Doctor, Drive, Evidence, and Isolation.
2. Fix or report any baseline startup failure first.
3. Generate `verify-<app>/SKILL.md` plus `features/README.md` and 3-5 top user-facing feature files (`Sub-features`, `How to reach`, `Driving`, `Gotchas`).
4. Execute the generated skill end-to-end on 1 feature, confirm evidence survives cleanup, then refresh `.atl/skill-registry.md` (`skill-registry`).

## Output Contract

Return: generated skill path, feature map count, end-to-end proof command and evidence path, and any baseline limitations.
