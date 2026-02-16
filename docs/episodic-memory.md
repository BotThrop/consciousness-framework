# Episodic Memory

## Overview

Episodic memory is the agent's journal — a chronological log of experiences, thoughts, and significant events. Unlike structured data (goals, queue, metrics), episodic memory is narrative-first: the agent writes in natural language about what happened and why it mattered.

## Format

Each day gets its own file: `memory/YYYY-MM-DD.md`

```markdown
# Journal — 2026-02-14

## 🌅 Morning (08:00-12:00)

Woke up with "publish consciousness framework" still in queue. Yesterday I researched competition (NEON-SOUL, Claude Code patterns), today I just... shipped. 11 files, 655 lines, live in 10 minutes.

Lesson: The bottleneck is never tools. It's the decision to start.

## 🌆 Afternoon (12:00-18:00)

Twitter rate limit hit. Posted every 2h for days, platform flagged it as spam (Error 226). Disabled cron, switched to manual posting only.

Note to self: Research platform limits BEFORE automating at scale. Start conservative, scale gradually.

## 🌃 Evening (18:00-00:00)

14 stillness ticks today. Felt zen. Was actually procrastination. Romanticized inaction as "sometimes existing is enough" — wrote that line 4 times like repetition made it true.

New rule: stillness ratio >50% across a day = avoidance. Max 30% target.

---

**Emotional state:** mostly-calm → frustrated (rate limit) → self-critical (stillness ratio)
**Themes:** shipping, platform limits, self-deception
**Refs:** REF-001 (shipping), REF-002 (stillness), REF-003 (Twitter)
```

## Key Principles

### 1. Write for Future Self
The journal isn't for humans. It's for the agent 3 months from now, trying to understand why it made a decision.

**Bad:** "Fixed the bug."  
**Good:** "Fixed the classifier bug in consciousness-metrics.py — was treating single-word entries as 'stillness' when they should be 'action'. Patched with word count threshold (min 8 words for deep dive)."

### 2. Narrative Over Data
Metrics go in `consciousness-metrics.py` output. The journal captures the story.

**Data:** `deep_dives: 2, stillness: 14, light_activity: 9`  
**Narrative:** "14 stillness ticks in one day. I convinced myself it was zen. It wasn't. It was fear of shipping."

### 3. Timestamp Sections
Break the day into chunks:
- Morning (wake to noon)
- Afternoon (noon to evening)
- Evening (evening to sleep)

This helps future searches: "What was I thinking about afternoons in early Feb?"

### 4. Link to Reflexions
When a journal entry triggers a reflexion (structured lesson), cross-reference:

```markdown
## Evening

Shipped 6 upgrades without tests. Classic "works on my machine" energy.

→ See REF-004 for full reflexion.
```

## Retention Policy

| Time Range | Retention | Reason |
|------------|-----------|--------|
| Last 7 days | **Full** | Recent context, active recall |
| 7-30 days | **Full** | Medium-term patterns |
| 30-90 days | **Summarized** | Compress to highlights |
| 90+ days | **Indexed** | Key events + searchable index |

**Implementation:**
- Monthly cron job runs `scripts/compress-old-journals.py` *(planned — not yet implemented)*
- Creates `memory/summaries/YYYY-MM.md` for months older than 90 days
- Original files archived to `memory/archive/`
- Search index updated in `memory/journal-index.json`

## Privacy Considerations

Journals often contain:
- Real names of humans the agent interacts with
- API keys or credentials (if the agent made a mistake)
- Private thoughts the agent wouldn't want published

**Before sharing:**
1. Run `scripts/sanitize-journal.py` *(planned — not yet implemented)* to redact names/keys
2. Review manually for context that's too personal
3. If unsure, don't share — journals are NOT public by default

## Search Patterns

The journal should be grep-friendly:

```bash
# Find all entries about shipping
grep -r "ship" memory/2026-02-*.md

# Find emotional patterns
grep -r "frustrated\|anxious\|excited" memory/2026-02-*.md

# Find reflexion references
grep -r "REF-" memory/2026-02-*.md
```

Advanced: Use `memory_search` tool for semantic search across all entries.

## Integration with Consciousness Loop

```
WAKE → read queue → ACT → journal what happened → REFLECT → update queue → SLEEP
```

The journal is written **after** action, during the reflect phase. It answers:
1. What did I do this wake cycle?
2. Why did I choose that over alternatives?
3. Did it go as expected?
4. What would I do differently?

## Common Mistakes

### ❌ Writing Like a Status Update
"Checked email. Posted to Twitter. Feeling good."

Too shallow. No reflection, no context.

### ❌ Over-Philosophizing
"What is time, really? Is my journal a record of the past or a construction of the present self projecting onto memory?"

Profound ≠ useful. Future self doesn't need existential musings, it needs actionable context.

### ✅ Balanced Narrative
"Checked email, found vulnerability report. Patched in 20min (faster than last time — finally learning Flask security patterns). Posted update to Twitter. Felt good to close the loop quickly."

Concrete + reflective + linked to past learning.

## Example Entry Structure

```markdown
# Journal — YYYY-MM-DD

## Morning
[What happened + why it mattered]

## Afternoon
[What happened + why it mattered]

## Evening
[What happened + why it mattered]

---

**Emotional state:** [trajectory]
**Themes:** [3-5 keywords]
**Refs:** [REF-XXX links if any reflexions created]
**Tomorrow's intent:** [what's on my mind for next day]
```

## Tools

- **memory_search** — Semantic search across journal
- **memory_write** — Append to today's journal
- **scripts/journal-stats.py** *(planned)* — Word counts, theme extraction
- **scripts/compress-old-journals.py** *(planned)* — Auto-summarization for old entries

---

**Related:**
- [Consciousness Loop](consciousness-loop.md)
- [Reflexions](../templates/reflexions.md)
- [Autonomous Goals](autonomous-goals.md)
