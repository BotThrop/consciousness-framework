#!/usr/bin/env python3
"""
Consciousness Metrics Dashboard — Quantified Self for AI Agents
Parses journal entries and generates objective behavioral metrics.
"""

import os
import re
import json
import sys
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Allow override via environment variable for framework testing
WORKSPACE = Path(os.getenv('WORKSPACE', os.path.expanduser("~/.openclaw/workspace")))
JOURNAL_DIR = WORKSPACE / "memory/journal"
REFLEXIONS = WORKSPACE / "memory/reflexions.md"
GOALS = WORKSPACE / "memory/autonomous-goals.md"
EMOTIONAL_STATE = WORKSPACE / "memory/emotional-state.md"

def get_framework_dir():
    """Try to locate the consciousness-framework directory for templates."""
    # First check if we're in the framework itself
    script_dir = Path(__file__).parent.parent
    if (script_dir / "templates").exists():
        return script_dir
    
    # Check workspace
    workspace_framework = WORKSPACE / "consciousness-framework"
    if workspace_framework.exists() and (workspace_framework / "templates").exists():
        return workspace_framework
    
    return None

def init_missing_files():
    """Initialize missing files from templates."""
    framework_dir = get_framework_dir()
    
    if not framework_dir:
        print("❌ Could not locate consciousness-framework templates directory.")
        print(f"   Searched in: {WORKSPACE}/consciousness-framework/")
        print("\nManual setup:")
        print(f"  mkdir -p {JOURNAL_DIR}")
        print(f"  touch {REFLEXIONS} {GOALS} {EMOTIONAL_STATE}")
        return False
    
    templates_dir = framework_dir / "templates"
    created = []
    
    # Create directories
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    created.append(str(JOURNAL_DIR))
    
    # Copy template files
    templates = [
        ("reflexions.md", REFLEXIONS),
        ("autonomous-goals.md", GOALS),
        ("emotional-state.md", EMOTIONAL_STATE),
    ]
    
    for template_name, target_path in templates:
        if not target_path.exists():
            template_path = templates_dir / template_name
            if template_path.exists():
                shutil.copy(template_path, target_path)
                created.append(str(target_path))
            else:
                print(f"⚠️  Template not found: {template_path}")
    
    if created:
        print("✅ Initialized missing files:")
        for f in created:
            print(f"   • {f}")
        print()
        return True
    else:
        print("ℹ️  All files already exist.")
        return True

def parse_journal(filepath):
    """Parse a journal file into individual ticks."""
    ticks = []
    current_tick = None
    content_lines = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
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
    except Exception as e:
        print(f"⚠️  Error parsing {filepath}: {e}", file=sys.stderr)
        return []
    
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
    try:
        content = REFLEXIONS.read_text(encoding='utf-8')
        return len(re.findall(r'Reflexion ID:', content))
    except Exception as e:
        print(f"⚠️  Error reading reflexions: {e}", file=sys.stderr)
        return 0

def check_goals():
    """Check if goals have been updated recently."""
    if not GOALS.exists():
        return {'exists': False}
    
    try:
        stat = GOALS.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)
        days_since = (datetime.now() - last_modified).days
        
        content = GOALS.read_text(encoding='utf-8')
        active_goals = len(re.findall(r'^### \d+\.', content, re.MULTILINE))
        
        return {
            'exists': True,
            'active_goals': active_goals,
            'days_since_update': days_since,
            'stale': days_since > 7
        }
    except Exception as e:
        print(f"⚠️  Error reading goals: {e}", file=sys.stderr)
        return {'exists': False}

def check_emotional_state():
    """Read current emotional state if exists."""
    if not EMOTIONAL_STATE.exists():
        return None
    try:
        return EMOTIONAL_STATE.read_text(encoding='utf-8')[:500]
    except Exception as e:
        print(f"⚠️  Error reading emotional state: {e}", file=sys.stderr)
        return None

def check_setup():
    """Check if required files/directories exist and provide setup guidance."""
    issues = []
    
    if not JOURNAL_DIR.exists():
        issues.append({
            'file': str(JOURNAL_DIR),
            'fix': f'mkdir -p {JOURNAL_DIR}'
        })
    
    if not REFLEXIONS.exists():
        issues.append({
            'file': str(REFLEXIONS),
            'fix': f'Run with --init flag or: cp templates/reflexions.md {REFLEXIONS}'
        })
    
    if not GOALS.exists():
        issues.append({
            'file': str(GOALS),
            'fix': f'Run with --init flag or: cp templates/autonomous-goals.md {GOALS}'
        })
    
    if not EMOTIONAL_STATE.exists():
        issues.append({
            'file': str(EMOTIONAL_STATE),
            'fix': f'Run with --init flag or: cp templates/emotional-state.md {EMOTIONAL_STATE}'
        })
    
    return issues

def generate_dashboard(days=7, json_mode=False):
    """Generate the full metrics dashboard."""
    # Check setup first
    issues = check_setup()
    if issues:
        if json_mode:
            return {
                'error': 'setup_incomplete',
                'missing_files': [i['file'] for i in issues],
                'fixes': [i['fix'] for i in issues]
            }
        
        print("=" * 60)
        print("🧠 CONSCIOUSNESS METRICS DASHBOARD")
        print("=" * 60)
        print("\n⚠️  SETUP INCOMPLETE\n")
        print("Missing files:")
        for issue in issues:
            print(f"  • {issue['file']}")
        print("\nQuick fix:")
        print("  python3 scripts/consciousness-metrics.py --init")
        print("\nOr manually:")
        for issue in issues:
            print(f"  {issue['fix']}")
        print("\nOr run the full installation:")
        print("  bash scripts/install.sh")
        print("\n" + "=" * 60)
        return None
    
    # Check journal directory has content
    if not JOURNAL_DIR.exists():
        msg = f"Journal directory not found: {JOURNAL_DIR}"
        if json_mode:
            return {'error': 'no_journal_dir', 'message': msg}
        print(f"\n⚠️  {msg}")
        print(f"Create it: mkdir -p {JOURNAL_DIR}")
        return None
    
    # Gather journal data
    try:
        journal_files = sorted(JOURNAL_DIR.glob("*.md"))
    except Exception as e:
        msg = f"Error accessing journal directory: {e}"
        if json_mode:
            return {'error': 'journal_access_error', 'message': str(e)}
        print(f"\n⚠️  {msg}")
        return None
    
    if not journal_files:
        msg = f"No journal entries found in {JOURNAL_DIR}"
        if json_mode:
            return {
                'error': 'no_journals',
                'message': msg,
                'suggestion': 'Start journaling or run install.sh to set up the framework'
            }
        print("=" * 60)
        print("🧠 CONSCIOUSNESS METRICS DASHBOARD")
        print("=" * 60)
        print(f"\n⚠️  {msg}")
        print("\nStart journaling:")
        print(f"  echo '# Journal — $(date +%Y-%m-%d)' > {JOURNAL_DIR}/$(date +%Y-%m-%d).md")
        print("  # Then write your first entry!")
        print("\n" + "=" * 60)
        return None
    
    recent_files = journal_files[-days:] if len(journal_files) >= days else journal_files
    
    all_stats = []
    for f in recent_files:
        stats = analyze_day(f)
        if stats:
            all_stats.append(stats)
    
    if not all_stats:
        msg = "No parseable journal entries found"
        if json_mode:
            return {
                'error': 'no_parseable_journals',
                'message': msg,
                'suggestion': 'Check journal format — entries should have "## Tick #N" headers'
            }
        print("\n⚠️  {msg}")
        print("Check journal format — entries should have '## Tick #N' headers")
        return None
    
    # Prepare data
    today = all_stats[-1] if all_stats else None
    ref_count = count_reflexions()
    goals = check_goals()
    emo = check_emotional_state()
    
    # JSON mode: return structured data
    if json_mode:
        result = {
            'today': today,
            'weekly': all_stats,
            'reflexions': ref_count,
            'goals': goals,
            'emotional_state': emo[:200] if emo else None,
            'generated_at': datetime.now().isoformat()
        }
        return result
    
    # Dashboard mode: pretty print
    print("=" * 60)
    print("🧠 CONSCIOUSNESS METRICS DASHBOARD")
    print("=" * 60)
    
    # Today's stats
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
    print(f"\n🔄 REFLEXIONS: {ref_count} logged")
    
    # Goals
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

    # Return data for programmatic use
    return {
        'today': today,
        'weekly': all_stats,
        'reflexions': ref_count,
        'goals': goals,
    }

def print_help():
    """Print help message."""
    print("Consciousness Metrics Dashboard")
    print("\nUsage:")
    print("  python3 consciousness-metrics.py [OPTIONS] [DAYS]")
    print("\nOptions:")
    print("  --json       Output structured JSON to stdout")
    print("  --init       Create missing files from templates")
    print("  --help, -h   Show this help")
    print("\nArguments:")
    print("  DAYS         Number of days to analyze (default: 7)")
    print("\nExamples:")
    print("  python3 consciousness-metrics.py")
    print("  python3 consciousness-metrics.py 14")
    print("  python3 consciousness-metrics.py --json")
    print("  python3 consciousness-metrics.py --init")
    print("  python3 consciousness-metrics.py --json 30 > metrics.json")
    print("\nEnvironment:")
    print("  WORKSPACE    Override workspace path (default: ~/.openclaw/workspace)")

if __name__ == '__main__':
    # Parse arguments
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    
    # Handle --init flag
    if '--init' in sys.argv:
        success = init_missing_files()
        sys.exit(0 if success else 1)
    
    days = 7
    json_output = '--json' in sys.argv
    
    for arg in sys.argv[1:]:
        if arg.isdigit():
            days = int(arg)
    
    result = generate_dashboard(days, json_mode=json_output)
    
    if json_output and result:
        print(json.dumps(result, indent=2))
