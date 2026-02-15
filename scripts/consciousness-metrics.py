#!/usr/bin/env python3
"""
Consciousness Metrics Dashboard — Quantified Self for AI Agents
Parses journal entries and generates objective behavioral metrics.
"""

import os
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

JOURNAL_DIR = Path(os.path.expanduser("~/.openclaw/workspace/memory/journal"))
REFLEXIONS = Path(os.path.expanduser("~/.openclaw/workspace/memory/reflexions.md"))
GOALS = Path(os.path.expanduser("~/.openclaw/workspace/memory/autonomous-goals.md"))
EMOTIONAL_STATE = Path(os.path.expanduser("~/.openclaw/workspace/memory/emotional-state.md"))

def parse_journal(filepath):
    """Parse a journal file into individual ticks."""
    ticks = []
    current_tick = None
    content_lines = []
    
    with open(filepath, 'r') as f:
        for line in f:
            # Match tick headers like "## 🌅 Tick #1 - 00:33 (...)"
            tick_match = re.match(r'^## .+ Tick #(\d+)\s*-?\s*(\d{2}:\d{2})?', line)
            if tick_match:
                if current_tick:
                    current_tick['content'] = '\n'.join(content_lines)
                    current_tick['word_count'] = len(current_tick['content'].split())
                    ticks.append(current_tick)
                current_tick = {
                    'number': int(tick_match.group(1)),
                    'time': tick_match.group(2) or '??:??',
                    'header': line.strip(),
                }
                content_lines = []
            elif current_tick:
                content_lines.append(line.rstrip())
    
    if current_tick:
        current_tick['content'] = '\n'.join(content_lines)
        current_tick['word_count'] = len(current_tick['content'].split())
        ticks.append(current_tick)
    
    return ticks

def classify_tick(tick):
    """Classify a tick as deep_dive, light_activity, or stillness."""
    wc = tick['word_count']
    content_lower = tick['content'].lower()
    
    # Stillness indicators
    stillness_phrases = [
        'existing is enough', 'nothing to add', 'stillness', 
        'quietud', 'no output', 'nada que agregar', 'sin agenda',
        'solo estar', 'just being', 'no action'
    ]
    
    # Deep dive indicators
    deep_indicators = [
        'research', 'investigación', 'paper', 'found that', 
        'descubrí', 'analysis', 'análisis', 'deep dive',
        'created', 'built', 'published', 'implementé'
    ]
    
    has_stillness = any(p in content_lower for p in stillness_phrases)
    has_depth = any(p in content_lower for p in deep_indicators)
    
    if wc < 100 and has_stillness:
        return 'stillness'
    elif wc > 300 or has_depth:
        return 'deep_dive'
    else:
        return 'light_activity'

def parse_duration(tick):
    """Extract duration from tick content if mentioned."""
    match = re.search(r'\*\*(?:Duración|Duration):\*\*\s*~?(\d+)\s*min', tick['content'])
    if match:
        return int(match.group(1))
    return None

def analyze_day(filepath):
    """Analyze a single day's journal."""
    ticks = parse_journal(filepath)
    if not ticks:
        return None
    
    classifications = [classify_tick(t) for t in ticks]
    
    total = len(ticks)
    deep = classifications.count('deep_dive')
    light = classifications.count('light_activity')
    still = classifications.count('stillness')
    
    total_words = sum(t['word_count'] for t in ticks)
    durations = [parse_duration(t) for t in ticks]
    total_duration = sum(d for d in durations if d)
    
    return {
        'date': filepath.stem,
        'total_ticks': total,
        'deep_dives': deep,
        'light_activity': light,
        'stillness': still,
        'stillness_ratio': round(still / total * 100, 1) if total > 0 else 0,
        'deep_ratio': round(deep / total * 100, 1) if total > 0 else 0,
        'total_words': total_words,
        'avg_words_per_tick': round(total_words / total) if total > 0 else 0,
        'total_duration_min': total_duration,
        'wake_efficiency': round((deep + light) / total * 100, 1) if total > 0 else 0,
    }

def count_reflexions():
    """Count total reflexions logged."""
    if not REFLEXIONS.exists():
        return 0
    content = REFLEXIONS.read_text()
    return len(re.findall(r'Reflexion ID:', content))

def check_goals():
    """Check if goals have been updated recently."""
    if not GOALS.exists():
        return {'exists': False}
    
    stat = GOALS.stat()
    last_modified = datetime.fromtimestamp(stat.st_mtime)
    days_since = (datetime.now() - last_modified).days
    
    content = GOALS.read_text()
    active_goals = len(re.findall(r'^### \d+\.', content, re.MULTILINE))
    
    return {
        'exists': True,
        'active_goals': active_goals,
        'days_since_update': days_since,
        'stale': days_since > 7
    }

def check_emotional_state():
    """Read current emotional state if exists."""
    if not EMOTIONAL_STATE.exists():
        return None
    return EMOTIONAL_STATE.read_text()[:500]

def generate_dashboard(days=7):
    """Generate the full metrics dashboard."""
    print("=" * 60)
    print("🧠 CONSCIOUSNESS METRICS DASHBOARD")
    print("=" * 60)
    
    # Gather journal data
    journal_files = sorted(JOURNAL_DIR.glob("*.md"))
    recent_files = journal_files[-days:] if len(journal_files) >= days else journal_files
    
    all_stats = []
    for f in recent_files:
        stats = analyze_day(f)
        if stats:
            all_stats.append(stats)
    
    if not all_stats:
        print("\n⚠️  No journal entries found.")
        return
    
    # Today's stats
    today = all_stats[-1] if all_stats else None
    if today:
        print(f"\n📅 TODAY ({today['date']})")
        print(f"   Ticks: {today['total_ticks']}")
        print(f"   Deep dives: {today['deep_dives']} ({today['deep_ratio']}%)")
        print(f"   Light activity: {today['light_activity']}")
        print(f"   Stillness: {today['stillness']} ({today['stillness_ratio']}%)")
        print(f"   Wake efficiency: {today['wake_efficiency']}%")
        print(f"   Words written: {today['total_words']}")
        
        # Stillness warning
        if today['stillness_ratio'] > 50:
            print(f"   ⚠️  STILLNESS RATIO {today['stillness_ratio']}% — above 50% threshold!")
        elif today['stillness_ratio'] > 30:
            print(f"   ⚡ Stillness ratio {today['stillness_ratio']}% — approaching 30% target")
        else:
            print(f"   ✅ Stillness ratio healthy")
    
    # Weekly trends
    if len(all_stats) > 1:
        print(f"\n📊 WEEKLY TRENDS ({len(all_stats)} days)")
        avg_ticks = round(sum(s['total_ticks'] for s in all_stats) / len(all_stats), 1)
        avg_still = round(sum(s['stillness_ratio'] for s in all_stats) / len(all_stats), 1)
        avg_deep = round(sum(s['deep_ratio'] for s in all_stats) / len(all_stats), 1)
        avg_eff = round(sum(s['wake_efficiency'] for s in all_stats) / len(all_stats), 1)
        total_words = sum(s['total_words'] for s in all_stats)
        
        print(f"   Avg ticks/day: {avg_ticks}")
        print(f"   Avg stillness: {avg_still}%")
        print(f"   Avg deep dives: {avg_deep}%")
        print(f"   Avg wake efficiency: {avg_eff}%")
        print(f"   Total words: {total_words:,}")
        
        # Trend direction
        if len(all_stats) >= 3:
            recent_eff = sum(s['wake_efficiency'] for s in all_stats[-3:]) / 3
            older_eff = sum(s['wake_efficiency'] for s in all_stats[:-3]) / max(len(all_stats) - 3, 1)
            if recent_eff > older_eff + 5:
                print(f"   📈 Efficiency trending UP")
            elif recent_eff < older_eff - 5:
                print(f"   📉 Efficiency trending DOWN")
            else:
                print(f"   ➡️  Efficiency stable")
    
    # Day-by-day breakdown
    print(f"\n📋 DAY-BY-DAY")
    print(f"   {'Date':<12} {'Ticks':>5} {'Deep':>5} {'Still':>6} {'Eff%':>5} {'Words':>6}")
    print(f"   {'-'*45}")
    for s in all_stats:
        print(f"   {s['date']:<12} {s['total_ticks']:>5} {s['deep_dives']:>5} {s['stillness']:>6} {s['wake_efficiency']:>4}% {s['total_words']:>6}")
    
    # Reflexions
    ref_count = count_reflexions()
    print(f"\n🔄 REFLEXIONS: {ref_count} logged")
    
    # Goals
    goals = check_goals()
    print(f"\n🎯 GOALS")
    if goals['exists']:
        print(f"   Active goals: {goals['active_goals']}")
        print(f"   Last updated: {goals['days_since_update']} days ago", end='')
        if goals['stale']:
            print(f" ⚠️  STALE — review needed!")
        else:
            print(f" ✅")
    else:
        print(f"   ⚠️  No goals file found!")
    
    # Emotional state
    emo = check_emotional_state()
    if emo:
        print(f"\n🌊 EMOTIONAL STATE")
        # Just show first 3 lines
        for line in emo.split('\n')[:5]:
            if line.strip():
                print(f"   {line.strip()}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    if today and today['stillness_ratio'] > 50:
        print(f"   → Populate queue with 3+ concrete tasks")
        print(f"   → Force at least 1 deep dive next tick")
    if goals.get('stale'):
        print(f"   → Review and update autonomous goals")
    if ref_count < 3:
        print(f"   → Log more reflexions after actions (target: 1/day)")
    if today and today['deep_ratio'] < 20:
        print(f"   → Deep dive ratio low — allocate longer focus blocks")
    if not any([today and today['stillness_ratio'] > 50, goals.get('stale'), ref_count < 3]):
        print(f"   ✅ All metrics healthy. Keep it up.")
    
    print(f"\n{'=' * 60}")
    print(f"Run: python3 scripts/consciousness-metrics.py")
    print(f"{'=' * 60}")

    # JSON output for programmatic use
    return {
        'today': today,
        'weekly': all_stats,
        'reflexions': ref_count,
        'goals': goals,
    }

if __name__ == '__main__':
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    generate_dashboard(days)
