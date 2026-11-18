# Playbook: Autonomous Run

**Goal:** Drive a scoped task to a falsifiable done predicate without stalling or looping.

1. **Lock the predicate:** State a deterministic done check. Create `odd/tasks/<feature>.md` when the task fails the Resume Test.
2. **Audit trail:** Use `show-me-your-work` only for multi-hour unattended runs.
3. **Execute:** Run and check each unit before the next. Work-unit commits follow odd-protocol section 6.
4. **Hard stops:** Pause only for irreversible external effects (force-push to shared branches, deploys, production data deletion, outside messages) or exhausted correction bounds.
5. **Close:** Close Sequence once over the full diff.

**Reply:** predicate status, units landed, verification, `Risk:` line, blockers.
