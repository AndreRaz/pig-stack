# Playbook: Authoring a Skill

**Goal:** Create or update an LLM-first `SKILL.md` that triggers reliably, stays compact, and enforces rules structurally.

1. **Format contract:** Write YAML frontmatter (`name`, single-line quoted `description` starting with `Trigger:` <= 250 chars, `license`, `metadata`), followed by `Activation Contract`, `Hard Rules`, `Decision Gates`, `Execution Steps`, `Output Contract`, and optional `References`.
2. **Token budget:** Target 180-450 tokens for `SKILL.md` (hard max 1000). Move templates, examples, and playbooks into `references/` or `playbooks/`.
3. **Imperative rules only:** Cut history, motivation, and generic advice. Point to local files and structural checks (`Encode Lessons in Structure`).
4. **Validate:** Refresh `.atl/skill-registry.md` and run `python3 scripts/validate_pig_stack.py` (or verify frontmatter + relative links).

**Reply:** skill path, trigger summary, token/validation status.
