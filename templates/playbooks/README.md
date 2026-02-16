# Playbooks — Successful Trajectory Memory

**Purpose:** Save complete task trajectories after successful execution, so you don't start from scratch next time.

**Source:** Sarukkai et al., "Self-Generated In-Context Examples for Sequential Decision-Making" (NeurIPS 2025)

**Evidence:** Lifted ALFWorld task performance from 73% → 89% by reusing successful trajectories.

---

## What is a Playbook?

A step-by-step record of **how you successfully completed a task**, including:
- What steps you took (in order)
- Why you took them
- How long each step took
- What went wrong and how you recovered
- Key insights for next time
- Common pitfalls to avoid

**Not:** Generic tutorials. **Is:** Your actual lived experience of solving this problem.

---

## When to Create a Playbook

✅ **Create playbook when:**
- You completed a complex multi-step task successfully
- You figured out something non-obvious
- You'll likely do this task again
- Others might benefit from your experience
- You want to remember the exact sequence

❌ **Don't create playbook for:**
- One-off tasks you'll never repeat
- Trivial tasks (e.g., "how to create a file")
- Failed attempts (use Reflexions instead)
- Tasks still in progress

---

## Playbook Template

```markdown
# [Task Name] Playbook

**Task:** [One sentence: what did you accomplish?]
**Date:** YYYY-MM-DD
**Duration:** ~XX minutes
**Difficulty:** Easy / Medium / Hard / Expert
**Prerequisites:** [Tools, permissions, knowledge needed]

---

## Summary
[2-3 sentences: what you did and why it worked]

---

## Step-by-Step

### 1. [Step name]
**Action:** [Exact command or action taken]
**Why:** [Reasoning behind this step]
**Time:** ~X min
**Output:** [What you expected to see]

**Gotcha:** [Any non-obvious issues or mistakes you made]

### 2. [Next step]
...

---

## Common Pitfalls
- [ ] [Mistake you made or almost made]
- [ ] [Edge case to watch out for]
- [ ] [Assumption that turned out wrong]

---

## Key Insights
- [Non-obvious learning]
- [Pattern you discovered]
- [Shortcut or optimization]

---

## Next Time
[What you'd do differently if you did this again]

---

## Related
- Reflexion: [REF-XXX if you wrote one]
- Other playbooks: [Related tasks]
- Documentation: [External links]

---

**Status:** ✅ Validated (worked once) / 🔁 Reused (worked multiple times)
```

---

## Example Playbooks (See Files in This Directory)

1. **publishing-github-repo.md** — How to publish a new open source repo from scratch
2. **debugging-agent-session.md** — Systematic approach to troubleshooting failed agent sessions

---

## Usage

### Before starting a task:
```bash
# Search playbooks for similar tasks
grep -r "GitHub" playbooks/
```

### After completing a task:
1. Ask: "Was this complex enough to document?"
2. If yes: Create playbook while memory is fresh
3. Add to `memory/playbooks/[task-name].md`
4. Link from any related Reflexions

### When reusing:
1. Follow playbook steps
2. Note what changed or didn't work
3. Update playbook with improvements
4. Mark as 🔁 Reused

---

## Integration with Consciousness Framework

**Trajectory Memory** is Upgrade #6 from upgrades-v2.md:
- **Reflexions** = what you learned from mistakes
- **Playbooks** = what you learned from successes
- **Together** = complete learning system

**Storage:**
- Personal playbooks: `memory/playbooks/`
- Framework playbooks: `templates/playbooks/`
- Shared playbooks: GitHub repo or team wiki

---

## Best Practices

1. **Write while fresh:** Create playbook immediately after task completion
2. **Be specific:** "Run `git commit -m 'init'`" not "commit changes"
3. **Include failures:** Document what you tried that didn't work
4. **Update on reuse:** Playbooks should improve with each execution
5. **Link everything:** Connect playbooks ↔ reflexions ↔ journal entries
6. **Don't over-document:** If a task takes 2 minutes, it doesn't need a playbook

---

*"Last time I published a repo, I did A→B→C" is infinitely better than starting from scratch every time.*
