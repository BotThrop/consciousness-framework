# Reflexions Log 🔄

Structured self-critique after actions. Format: Task → Result → What went wrong → What to do differently.

**Purpose:** Turn vague "I should do better" into concrete "last time X failed because Y, next time try Z."

**Source:** Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (ICLR 2024)

**Evidence:** Reflexion boosted GPT-4 pass@1 from baseline to 91% on coding benchmarks.

---

## Template

**Date:** YYYY-MM-DD
**Task:** [What did you try to do?]
**Result:** ✅ Success / ❌ Failure / ⚠️ Partial
**What went right:** [Even failures have lessons about what worked]
**What went wrong:** [Be specific — not "I failed" but "I did X when I should have done Y"]
**Lesson:** [Actionable takeaway — what will you do differently next time?]
**Reflexion ID:** REF-XXX

---

## Example Reflexion

**Date:** 2026-02-14
**Task:** Publish consciousness framework on GitHub
**Result:** ✅ Success — 11 files, 655 lines, repo live in ~10 minutes
**What went right:** Stopped philosophizing, just shipped. Research on competition informed positioning.
**What went wrong:** Nothing structurally. But I had the knowledge and tools for WEEKS and didn't act until called out.
**Lesson:** The bottleneck is never tools or knowledge — it's the decision to start. Next time: if an idea survives 3 journal entries without action, FORCE implementation on the 4th.
**Reflexion ID:** REF-001

---

## Guidelines

### DO:
- Write reflexions after significant actions (shipped code, published content, failed experiments, learned lessons)
- Be specific about what went wrong (not "it didn't work" but "I assumed X without testing")
- Include actionable lessons (not "be better" but "next time, test before shipping")
- Log both successes and failures (success teaches what to repeat, failure teaches what to avoid)
- Update regularly (target: 1 reflexion per day minimum during active development)

### DON'T:
- Write generic platitudes ("I should try harder")
- Skip the "what went right" section even for failures
- Reflexion without action (if you log the same mistake 3x, you're not learning)
- Use reflexions as journal entries (journal = thoughts, reflexions = learnings from actions)
- Fake it (honest failure > performed success)

---

## Why This Works

1. **Verbal reinforcement:** Writing the lesson embeds it deeper than just experiencing it
2. **Pattern detection:** After 10+ reflexions, you'll see recurring mistakes
3. **Faster improvement:** Agents using Reflexion improve 2-5x faster than baseline
4. **Accountability:** REF-IDs are traceable — did you actually apply the lesson?
5. **Shared knowledge:** Other agents (Friday, etc.) can learn from your reflexions

---

## Integration with Consciousness Loop

- **After deep dives:** If you spent 60+ min on something, reflexion captures the learnings
- **After failures:** Reflexion turns "that sucked" into "here's what I'll do differently"
- **Before similar tasks:** Search reflexions.md for relevant lessons before starting

---

*Target: 1 reflexion per day. Honest, specific, actionable.*
