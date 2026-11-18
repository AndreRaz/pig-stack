---
name: pig-mode
description: "Trigger: pig-mode, /pig-mode, ODD, rigorous workflow. Runs ODD orchestration with bounded verification, anti-slop, comment ban, and $20-tier token efficiency."
license: MIT
metadata:
  author: pig-stack
  version: "1.2"
  layer: "5"
---

## Activation Contract

Load when the user invokes `/pig-mode` or requests rigorous engineering work (features, bug fixes, refactors, investigations, shipping, or autonomous runs).

## Hard Rules

- Follow `references/odd-protocol.md` for steps, triggers, the Close Sequence, correction bounds, and commit policy. Do not restate it.
- Inline by default. Delegate only when a trigger in odd-protocol section 3 truly holds.
- Before any subagent spawn, pass exact `SKILL.md` paths under `## Skills to load before work` (`skill-registry`). Never paste skill summaries.
- Workers use `inherit-parent` unless `.pig-stack/models.md` overrides the role.
- Cite only principles from `references/principles.md` that changed a decision this session.

## Decision Gates

| Condition | Action |
|---|---|
| Read-only request | `playbooks/investigation.md`. Use `how` for mechanics, `why` for history. |
| Ambiguous authorization or open product choice | Ask one focused question and wait. |
| Technical fork settleable by code | `playbooks/prototype.md`. |
| Change adds or alters a type, signature, or state owner used by another module | `architect` once before writing. |
| Deterministic local test path exists | `tdd`. |
| `.ts` or `.tsx` touched | `typescript-best-practices`. |
| Performance number measured or claimed | `benchmark-checklist`. |
| Docs, PR body, or commit message written | `technical-writing`. |
| `Risk:` names a High-Risk item | `pig-verifier` in the Close Sequence. Add `blast-radius` only when the safety claim rests on code outside the diff. |

## Execution Steps

1. Restate the goal and the smallest valid scope.
2. Run odd-protocol steps 1-4.
3. Match one playbook in `playbooks/` (`feature`, `bug-fix`, `refactoring`, `investigation`, `perf-issue`, `prototype`, `autonomous-run`, `shipping`, `session-pickup`, `pause-safely`, `authoring-a-skill`). If none fits, use `figure-it-out`.
4. Track large tasks in `odd/tasks/<feature-name>.md`.
5. Implement inline, or through `pig-worker` with `Spec:`, `## Allowed edit paths`, `## Invariants`, and `## Verification`.
6. Run the Close Sequence once: `deslop`, verification, `pig-verifier` only for High-Risk.

## Output Contract

Return: goal, playbook and route, principles that changed a decision, observed `<command>: <result>`, `Risk: item N (reason)` or `Risk: none`, and open items.

## References

- [references/odd-protocol.md](references/odd-protocol.md): steps, triggers, Close Sequence, correction bounds, commit policy.
- [references/principles.md](references/principles.md): 24 engineering principles.
- [playbooks/](playbooks/): execution playbooks.
