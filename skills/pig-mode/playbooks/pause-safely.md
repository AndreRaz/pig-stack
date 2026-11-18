# Playbook: Pause Safely

**Goal:** Suspend work so any later session resumes with no lost context.

1. **Keep work:** Leave valid changes in place. Revert only a broken experiment that fails its checks, and log why.
2. **Record state:** Write progress, the last check with its result, blockers, and the next step in `odd/tasks/<feature>.md` under `## Log`. For a small task with no feature document, put the same facts in the reply.
3. **No new commits:** Commit only when odd-protocol section 6 already allows it. Otherwise list the uncommitted paths from `git status`.

**Reply:** where state is saved, the last observed check, and the exact next step.
