# pig-stack Repository Instructions

This repository implements `pig-stack`, a multi-runtime ODD + anti-slop engineering plugin.

## Authoring Rules

- Keep every `SKILL.md` in LLM-first format: YAML frontmatter (`name`, single-line quoted `description` starting with `Trigger:` <= 250 chars, `license`, `metadata`), followed by `Activation Contract`, `Hard Rules`, `Decision Gates`, `Execution Steps`, `Output Contract`, and optional `References`.
- Target 180-450 tokens per `SKILL.md` body (hard cap 1000 tokens). Move long playbooks and reference tables into local `references/` or `playbooks/` subdirectories.
- Keep scripts and tests free of explanatory comments (comment ban enforced by validator).
- Never reference external Cursor-only plugins or hardcode proprietary model slugs.

## Verification Gate

After any edit to manifests, skills, agents, docs, or scripts, run:

```bash
python3 scripts/generate_registry.py
python3 scripts/validate_pig_stack.py
python3 -m unittest discover -s tests -v
```
