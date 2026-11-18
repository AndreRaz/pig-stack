---
name: skill-registry
description: "Trigger: skill-registry, update skills, refresh registry, skill resolver. Indexes available SKILL.md files and injects exact paths before subagent delegation."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "5"
---

## Activation Contract

Load after creating, moving, or updating skills, or when resolving exact `SKILL.md` paths prior to spawning subagents.

## Hard Rules

- **Index only, never summarize:** `.atl/skill-registry.md` stores `name`, `Trigger / description`, `scope`, and exact `path`. Subagents read the full `SKILL.md` so intent never degrades.
- **Deterministic generation:** Use `python3 scripts/generate_registry.py` when present instead of hand-writing the index.
- **Cap injected paths:** Pass at most 5 matching `SKILL.md` paths per subagent launch under `## Skills to load before work`, prioritizing file/code context over general workflow skills.
- **Self-correct on fallback:** If a subagent returns `skill_resolution` other than `paths-injected`, re-read `.atl/skill-registry.md` before the next delegation.

## Decision Gates

| Situation | Action |
|---|---|
| `scripts/generate_registry.py` exists | Run it to update `.atl/skill-registry.md`. |
| No generator script in target repo | Scan `./skills`, `.agents/skills`, `.cursor/skills`, `.claude/skills` read-only and select exact paths. |
| Same skill name exists in project and globally | Project skill overrides global skill. |

## Execution Steps

1. Refresh or read `.atl/skill-registry.md`.
2. Match the delegated task's file extensions and actions against the `Trigger` column (max 5 skills).
3. Inject exact paths in the subagent brief under `## Skills to load before work`.

## Output Contract

Return: registry path, indexed skill count, and exact `SKILL.md` paths selected for delegation (if delegating).
