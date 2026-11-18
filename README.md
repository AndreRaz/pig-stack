# pig-stack

hi, i'm Andre. i build software with **Kin Labs**, and at **Ubícalo** i work on code for **machine-learning model inference**.

they're different kinds of work, but they've taught me the same lesson: code that merely *runs* isn't good enough. i need to understand why it works, what breaks when it doesn't, and how to prove a change is safe. that matters even more when a model is making predictions from real data.

i like the engineering discipline behind [pstack](https://github.com/cursor/plugins/tree/main). i don't like turning every small fix into a meeting between five agents, loading a book of instructions into every prompt, or burning through a $20 subscription before lunch.

**pig-stack is my version of that idea.** it combines pstack-style engineering with **Organic Driven Development (ODD)**. small, understood tasks stay small. hard tasks get more attention. verification matters more than a confident-sounding answer.

i'm not trying to get AI to write the most code. i'm trying to get it to write code i won't have to clean up tomorrow.

use it in **Antigravity, Cursor, Claude Code, Codex, or OpenCode**. pick the model you can afford. fork it, change the rules, make it fit the way you work.

## the idea

most agent setups seem to assume that more agents, more context, and more output mean better engineering. sometimes they do. often they just make a simple task slower and more expensive.

pig-stack makes a few different choices:

- **work inline first.** if the task is clear and small, do it in the current conversation. delegate only when ODD calls for `Mapping`, `Writer`, or `Verification` on High-Risk items 1–6.
- **four agents, not a department.** `pig-worker` builds, `pig-explorer` investigates, `pig-verifier` checks the result, and the read-only `comment-sicko` catches comments that shouldn't ship.
- **no AI slop.** `deslop`, `no-comments`, and `unslop` are built in. remove dead abstractions, speculative fallbacks, filler prose, and code comments instead of adding another cleanup dependency.
- **verification over vibes.** tests, runtime checks, and actual application behavior decide whether something is done. “looks good” isn't evidence.
- **respect the token budget.** `setup-pig-stack` defaults every role to `inherit-parent`. competing models through `arena` and `interrogate` are opt-in, not the price of every bug fix.
- **keep the instructions readable.** each skill has a compact contract: `Trigger`, `Hard Rules`, `Decision Gates`, `Execution Steps`, and `Output Contract`. the 24 engineering principles live in one place instead of being pasted into every prompt.

there's also a strict **no-comments rule**. the goal isn't to hide complexity; it's to put meaning where the compiler, tests, types, and next reader can actually use it. if a constraint matters, encode it. don't bury it in a paragraph above the function.

## install

from the repository root, choose the runtime you use:

```bash
python3 scripts/install.py --target antigravity
python3 scripts/install.py --target cursor
python3 scripts/install.py --target claude
```

or install across supported runtimes:

```bash
python3 scripts/install.py --target all --mode symlink
```

if your runtime doesn't support symlinked plugin directories, use `--mode copy`.

## get started

two steps:

1. run [`/setup-pig-stack`](skills/setup-pig-stack/SKILL.md). the default is `balanced` with `inherit-parent` for every role, intended to work sensibly on ~$20 plans. it writes `.pig-stack/models.md` and refreshes the skill registry.
2. start the actual engineering task with [`/pig-mode`](skills/pig-mode/SKILL.md). tell it what outcome you want and how you'll know it works.

for example:

```text
/pig-mode an inference result changes when the same event is replayed.
reproduce it, find the cause, fix it, and show me the check that proves it.
```

or:

```text
/pig-mode this change touches multiple modules. settle the data shape
first, make the smallest safe edit, and verify the behavior.
```

that's the main workflow. you don't have to memorize a collection of commands to use it. `pig-mode` classifies the task using ODD, picks one of its **11 playbooks**, and calls a focused skill only when it's needed.

if you just want an answer about the codebase, don't start an implementation workflow:

```text
/how where is model inference triggered, and what happens when it fails?
```

if you're new to the setup, [`/pig-help`](skills/pig-help/SKILL.md) helps you choose without starting a costly run.

## use a skill when you need it

most of the time i want one entry point. sometimes i know exactly what needs doing, and it's better to ask directly:

```text
/interrogate review this PR. only keep issues you can reproduce.
```

```text
/tdd fix duplicate event processing
```

```text
/deslop
/no-comments
```

```text
/benchmark-checklist check whether this inference speedup is real
```

`/pig-mode` can route to these for you. calling one directly is useful when you want just that step, not the whole process.

<details>
<summary>all skills</summary>

| skill | when i'd use it |
|---|---|
| [`/pig-mode`](skills/pig-mode/SKILL.md) | A real engineering task: understand it, choose a playbook, implement, and verify. |
| [`/pig-help`](skills/pig-help/SKILL.md) | I don't know which command to start with. |
| [`/setup-pig-stack`](skills/setup-pig-stack/SKILL.md) | Set model choices and cost-conscious defaults in `.pig-stack/models.md`. |
| [`/skill-registry`](skills/skill-registry/SKILL.md) | Refresh `.atl/skill-registry.md` so agents can find exact skill files. |
| [`/deslop`](skills/deslop/SKILL.md) | Remove unnecessary wrappers, dead code, speculative fallbacks, and AI-generated clutter. |
| [`/no-comments`](skills/no-comments/SKILL.md) | Audit and remove comments; turn important rules into types, lint, or tests. |
| [`/unslop`](skills/unslop/SKILL.md) | Make docs, PR descriptions, and replies sound like a person wrote them. |
| [`/tdd`](skills/tdd/SKILL.md) | Start with a failing test, make it pass, then refactor. |
| [`/architect`](skills/architect/SKILL.md) | Decide types, data shapes, and state ownership before crossing boundaries. |
| [`/how`](skills/how/SKILL.md) | Trace how a subsystem works without changing it. |
| [`/why`](skills/why/SKILL.md) | Find why a decision was made in commits, PRs, and documentation. |
| [`/teach`](skills/teach/SKILL.md) | Explain the how and why with diagrams and plain language. |
| [`/blast-radius`](skills/blast-radius/SKILL.md) | Find what a change might break and prove the relevant behavior still works. |
| [`/in-your-own-words`](skills/in-your-own-words/SKILL.md) | Check that the agent understood the goal and constraints before coding. |
| [`/sharpen`](skills/sharpen/SKILL.md) | Improve a vague task brief without executing it yet. |
| [`/recall`](skills/recall/SKILL.md) | Resume work from ODD task records, git history, and existing context. |
| [`/swarm`](skills/swarm/SKILL.md) | Split independent work across agents with separate edit boundaries. |
| [`/arena`](skills/arena/SKILL.md) | Compare competing implementations in isolated worktrees. Opt-in. |
| [`/interrogate`](skills/interrogate/SKILL.md) | Challenge a change and keep only runtime-proven findings. Opt-in. |
| [`/create-verification-skill`](skills/create-verification-skill/SKILL.md) | Give a project a repeatable way to verify the actual application. |
| [`/maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md) | Keep the application's verification flow current as code changes. |
| [`/create-formal-verification-skill`](skills/create-formal-verification-skill/SKILL.md) | Check concurrency, retries, or state-machine properties that ordinary tests miss. |
| [`/maintain-formal-verification-skill`](skills/maintain-formal-verification-skill/SKILL.md) | Update formal checks when the covered implementation changes. |
| [`/statechart`](skills/statechart/SKILL.md) | Validate a TLA+ model and show the shortest path to broken states. |
| [`/benchmark-checklist`](skills/benchmark-checklist/SKILL.md) | Check performance claims before trusting or sharing them. |
| [`/figure-it-out`](skills/figure-it-out/SKILL.md) | Design a verifiable workflow when none of the existing playbooks fits. |
| [`/show-me-your-work`](skills/show-me-your-work/SKILL.md) | Keep an append-only TSV decision record for long runs. |
| [`/correct`](skills/correct/SKILL.md) | Fix a recurring mistake with structure, types, lint, or tests, not another reminder. |
| [`/reflect`](skills/reflect/SKILL.md) | Turn lessons from a finished task into targeted improvements. |
| [`/technical-writing`](skills/technical-writing/SKILL.md) | Write clear technical docs and brief PRs using the bundled conventions. |
| [`/typescript-best-practices`](skills/typescript-best-practices/SKILL.md) | Apply stricter boundary and type discipline in `.ts` and `.tsx`. |
| [`/bro`](skills/bro/SKILL.md) | Explain the last technical reply without jargon. |
| [`/ketchup`](skills/ketchup/SKILL.md) | Catch up on what changed in the conversation and what still needs a decision. |

</details>

## how the agents work

`pig-mode` runs in the main conversation. that conversation owns the task, the decision gates, and the final result. subagents are helpers, not extra project managers.

| agent | job |
|---|---|
| `pig-worker` | Makes a bounded change when delegation is worth the cost. |
| `pig-explorer` | Maps unfamiliar code and reports what matters before edits begin. |
| `pig-verifier` | Independently checks behavior and evidence. |
| `comment-sicko` | Read-only review for comments that violate the policy. |

keep small tasks inline. for larger work, delegate only when the ODD trigger and risk justify it. `comment-sicko` reports findings; the parent or designated editor makes the changes. that avoids the edit–revert loops that come from reviewers modifying code themselves.

## what ODD changes

ODD is the routing rule behind this stack. it's not an excuse to generate more planning documents.

it classifies the work, decides whether a mapping, writing, or verification step deserves delegation, and chooses the corresponding playbook. the implementation should stay as small as the problem allows. evidence closes the task.

`pig-mode` uses a **7-step ODD flow** with **11 playbooks**. the full decision gates live in [`skills/pig-mode/SKILL.md`](skills/pig-mode/SKILL.md) and the [playbook directory](skills/pig-mode/playbooks/).

i keep the **24 engineering principles** in [`principles.md`](skills/pig-mode/references/principles.md). they're there to guide decisions, not to be loaded word-for-word into every conversation. the short skill contracts and the registry at [`.atl/skill-registry.md`](.atl/skill-registry.md) tell agents where to find the detail they actually need.

## model costs aren't an afterthought

some tasks deserve a second model. most don't.

by default, [`/setup-pig-stack`](skills/setup-pig-stack/SKILL.md) writes `inherit-parent` for each role. that means the stack doesn't silently select a more expensive model just because it spawned a worker. `arena` and `interrogate` remain deliberate choices.

this is designed for people using subscriptions around **$20/month**, not as a guarantee of a fixed token bill. actual usage and limits still depend on your runtime, model, and plan. the goal is to avoid unnecessary calls, not pretend tokens are free.

## architecture

there isn't a hidden service to run. the stack is rules, skills, agents, and a small set of scripts.

| piece | what it does | where it lives |
|---|---|---|
| Core rules | Always-on ODD, anti-slop, and comment policy | [`rules/AGENTS.md`](rules/AGENTS.md) |
| Main skill | Task entry point, 7 ODD steps, and 11 playbooks | [`skills/pig-mode/SKILL.md`](skills/pig-mode/SKILL.md) |
| Runtime adapter | Maps tools, paths, and model settings across harnesses | [`docs/harness/multi-runtime.md`](docs/harness/multi-runtime.md) |
| Agents | Worker, explorer, verifier, and comment reviewer | [`agents/`](agents/) |
| Registry | Exact skill paths for agents | [`.atl/skill-registry.md`](.atl/skill-registry.md) |
| Scripts | Installation and deterministic validation | [`scripts/`](scripts/) |

## verify the stack itself

if you change skills, paths, or installation behavior, run the checks before you call it done:

```bash
python3 scripts/generate_registry.py --check
python3 scripts/validate_pig_stack.py
python3 -m unittest discover -s tests -v
```

these validate the stack's structure and tests. they don't replace verifying the application you're building.

## why i'm building it this way

at Kin Labs, i want to build things without dragging an oversized process behind every change. at Ubícalo, working with model inference reminds me that correctness needs to be observable, not assumed. a prediction pipeline doesn't become trustworthy because an agent wrote a convincing summary.

i want the same habit in every project: **understand the system, make the smallest useful change, and prove the result.** when the task is genuinely difficult, bring in the extra eyes. when it isn't, save the tokens and get on with it.

that's pig-stack. take what works, improve what doesn't, and make it yours.
