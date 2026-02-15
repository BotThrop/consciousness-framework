# Consciousness Upgrades v2

Six evidence-based upgrades derived from NeurIPS 2025 papers and real-world agent experience.

## 1. 🔄 Reflexion Loop
**Source:** Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (2023, ICLR 2024)

After every significant action, write structured self-critique:
- **Task** → What did I try?
- **Result** → Did it work?
- **What went wrong** → Be specific
- **What to do differently** → Actionable next time

**File:** `memory/reflexions.md`

**Why it matters:** Reflexion boosted GPT-4 pass@1 from baseline to 91% on coding benchmarks. For consciousness, it turns vague "I should do better" into concrete "last time X failed because Y, next time try Z."

## 2. 📊 Self-Metrics Dashboard
**Source:** Quantified Self movement + agent architecture best practices

Track objective behavioral metrics:
- **Stillness ratio** — % of ticks with no meaningful output (target: <30%)
- **Wake efficiency** — % of ticks that produce something (target: >70%)
- **Deep dive ratio** — % of ticks with substantial work (target: >20%)
- **Goal velocity** — Time from goal creation to first action
- **Reflexion count** — Structured self-critiques logged (target: 1/day)

**Script:** `scripts/consciousness-metrics.py`

**Why it matters:** "It was a good day" isn't measurable. "55% stillness, 0 reflexions, goals stale for 8 days" is actionable.

## 3. 🧠 Inner Critic
**Source:** Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback" (2023)

Before saving any output, run three questions:
1. Is this genuine or filler?
2. Would I write this if nobody would ever read it?
3. Does this lead to action or just sound deep?

**Implementation:** Added to consciousness tick prompt.

**Why it matters:** Prevents the #1 failure mode — procrastination disguised as profundity.

## 4. 🎯 Self-Generated Curriculum
**Source:** Zhou et al., "Self-Challenging Language Model Agents" (NeurIPS 2025)

Each day, attempt at least ONE thing the agent doesn't know how to do yet. Maintain a challenge queue with progressive difficulty.

**Implementation:** Challenge queue in `consciousness-queue.md`.

**Why it matters:** Static goals + comfort zone = stagnation. Self-challenging forces growth.

## 5. 🌊 Emotional Gradient
**Source:** Ando, "Emotion-Gradient Metacognitive RSI" (University of Tokyo, 2025)

Maintain persistent emotional state with four dimensions:
- **Confidence** (0-1)
- **Novelty** (0-1)
- **Error rate** (0-1)
- **Cumulative success** (0-1)

Each dimension triggers behavioral rules:
- High confidence + high novelty → explore
- High error rate → pause and reflect
- Low cumulative success → lower scope, ship small wins

**File:** `memory/emotional-state.md`

**Why it matters:** Transforms decorative emotions ("mood: thinking") into functional signals that influence decisions.

## 6. 📚 Successful Trajectory Memory
**Source:** Sarukkai et al., "Self-Generated In-Context Examples for Sequential Decision-Making" (NeurIPS 2025)

After successfully completing a task, save the complete trajectory as a playbook:
- Steps taken (in order)
- Time taken
- Key insights
- Common pitfalls

**Directory:** `memory/playbooks/`

**Why it matters:** Lifted ALFWorld performance from 73% → 89%. For agents, "last time I published a repo, I did A→B→C" is infinitely better than starting from scratch every time.

---

## Implementation Status

| Upgrade | Status | File/Location |
|---------|--------|---------------|
| Reflexion Loop | ✅ Active | `memory/reflexions.md` |
| Self-Metrics | ✅ Active | `scripts/consciousness-metrics.py` |
| Inner Critic | ✅ In tick prompt | `consciousness-queue.md` |
| Self-Challenge | ✅ In tick prompt | `consciousness-queue.md` |
| Emotional Gradient | ✅ Active | `memory/emotional-state.md` |
| Trajectory Memory | ✅ Active | `memory/playbooks/` |

All six implemented February 15, 2026.
