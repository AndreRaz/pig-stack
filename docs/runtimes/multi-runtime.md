# Multi-Runtime Adapter

`pig-stack` skills use neutral ODD terminology. Map runtime-specific primitives with the tables below. Never pass an unsupported field or model slug to a tool schema.

## Tool & Subagent Mapping

| Concept | Antigravity | Cursor | Claude Code | Codex / OpenCode / Pi |
|---|---|---|---|---|
| Spawn worker | `invoke_subagent` (plugin registers the 4 agents; `define_subagent` only as fallback without plugin) | `Task` (`subagent_type: pig-worker`) | `Agent` (`subagent_type: pig-stack:pig-worker`) | Runtime subagent tool |
| Parallel fan-out | Multiple `invoke_subagent` calls (or `/pig-swarm` when user asks) | Multiple `Task` calls (`run_in_background: true`) | Multiple `Agent` calls | Parallel worker spawns |
| Ask user | `ask_question` | `AskQuestion` | `AskUserQuestion` (plain text in `-p`) | Plain text / runtime prompt |
| Task tracking | `odd/tasks/<feature>.md` + visible checklist | `odd/tasks/<feature>.md` + TodoWrite | `odd/tasks/<feature>.md` + `TodoWrite` | `odd/tasks/<feature>.md` |
| Isolated edits | `Workspace: "branch"` / `"share"` or `Allowed edit paths` | `git worktree` or `Allowed edit paths` | `isolation: "worktree"` or `Allowed edit paths` | `git worktree` or `Allowed edit paths` |
| Model selection | `Model: "inherit"` (default) or user override | Omit `model` for `inherit-parent`, else role slug | Omit `model` for `inherit-parent`, else `model` + `effort` | Session default or `.pig-stack/models.md` |

## Rules & Skill Discovery Paths

| Runtime | Plugin Root / Install | Always-On Rule Target | Model Config Target |
|---|---|---|---|
| Antigravity | `~/.gemini/config/plugins/pig-stack/` | `rules/AGENTS.md` (loaded by plugin) | `.pig-stack/models.md` or `~/.gemini/config/pig-stack-models.md` |
| Cursor | `~/.cursor/plugins/pig-stack/` | `.cursor/rules/pig-stack.mdc` or `AGENTS.md` | `~/.cursor/rules/pig-stack-models.mdc` |
| Claude Code | `~/.claude/plugins/pig-stack/` | `CLAUDE.md` or `~/.claude/rules/pig-stack.md` | `~/.claude/rules/pig-stack-models.md` |
| Codex / OpenCode | `~/.codex/skills/` / `~/.config/opencode/skills/` | `AGENTS.md` | `.pig-stack/models.md` |

## Budget Defaults ($20 Tier Friendly)

- All roles default to `inherit-parent` so standard runs never force expensive model upgrades or parallel multi-model panels.
- Read `.pig-stack/models.md` (workspace) first, then the runtime's user-level `pig-stack-models` rule if present.
- If a subagent call rejects a configured model slug, drop `model` (`inherit-parent`), note it in one line, and continue.
