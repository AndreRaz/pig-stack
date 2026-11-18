# Playbook: Session Pickup

**Goal:** Resume in-flight work accurately without losing prior specs, decisions, or uncommitted edits.

1. **Reconstruct state:** Check `git status`, `git log -n 10 --oneline`, and `odd/tasks/*.md` (plus Engram `mem_context` / `mem_search` if available). Use `recall` if context spans multiple sessions.
2. **Reconcile before editing:** Compare `odd/tasks/<feature>.md` (`## Specs`, `## Tasks`, `## Log`) against actual `git diff` and current test status. File state wins over stale memory.
3. **Continue from next unfinished task:** Hand off or execute the next open `T#` with its linked `S#`, preserving unrelated working-tree changes.

**Reply:** current branch/state capsule, reconciled tasks (`done` vs `pending`), and immediate action taken or proposed.
