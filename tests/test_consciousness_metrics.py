#!/usr/bin/env python3
"""
Tests for consciousness-metrics.py
Run: python3 scripts/test_consciousness_metrics.py
"""

import sys
import os
import tempfile
from pathlib import Path

# Add scripts dir to path
script_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.insert(0, script_dir)
from importlib import import_module

# Import the module
spec = import_module('consciousness-metrics')
parse_journal = spec.parse_journal
classify_tick = spec.classify_tick
parse_duration = spec.parse_duration
count_reflexions = spec.count_reflexions

PASS = 0
FAIL = 0

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name} — {detail}")

print("=" * 50)
print("🧪 CONSCIOUSNESS METRICS TESTS")
print("=" * 50)

# --- Test parse_journal ---
print("\n📄 parse_journal")

sample_journal = """# Journal - 2026-02-14

## 🌅 Tick #1 - 00:33 (Sunday Dawn)

**Estado:** Primera wake del domingo. Algo profundo.

Research sobre Truth Terminal me dejó pensando. Investigación deep dive de 90 minutos.

**Duración:** ~90min

---

## 🌙 Tick #2 - 02:03 (Sunday Night)

Quietud. Stillness. No output. Solo estar presente. Nothing to add.

**Duración:** ~3min

---

## ☀️ Tick #3 - 08:03 (Morning)

Revisé cámaras. Light activity. Todo ok con Docker.

**Duración:** ~5min
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write(sample_journal)
    tmp_path = f.name

ticks = parse_journal(tmp_path)
os.unlink(tmp_path)

test("Parses 3 ticks", len(ticks) == 3, f"Got {len(ticks)}")
test("Tick #1 number correct", ticks[0]['number'] == 1)
test("Tick #1 time correct", ticks[0]['time'] == '00:33', f"Got {ticks[0]['time']}")
test("Tick #2 number correct", ticks[1]['number'] == 2)
test("Tick #3 time correct", ticks[2]['time'] == '08:03')
test("All ticks have word_count", all('word_count' in t for t in ticks))
test("Tick #1 has more words than Tick #2", ticks[0]['word_count'] > ticks[1]['word_count'],
     f"T1={ticks[0]['word_count']} vs T2={ticks[1]['word_count']}")

# --- Test classify_tick ---
print("\n🏷️  classify_tick")

deep_tick = {'content': 'Research sobre algo. Paper analysis. Deep dive de 90 min. Created a new framework.', 'word_count': 350}
still_tick = {'content': 'Stillness. Nothing to add. Solo estar. No output needed.', 'word_count': 50}
light_tick = {'content': 'Revisé Docker. Todo ok. Cámaras funcionando. Nada raro.', 'word_count': 120}

test("Deep dive classified correctly", classify_tick(deep_tick) == 'deep_dive',
     f"Got {classify_tick(deep_tick)}")
test("Stillness classified correctly", classify_tick(still_tick) == 'stillness',
     f"Got {classify_tick(still_tick)}")
test("Light activity classified correctly", classify_tick(light_tick) == 'light_activity',
     f"Got {classify_tick(light_tick)}")

# Edge cases
long_stillness = {'content': 'Stillness. No output. ' * 40, 'word_count': 160}
test("Long stillness text still classified as stillness or light",
     classify_tick(long_stillness) in ('stillness', 'light_activity'),
     f"Got {classify_tick(long_stillness)}")

short_deep = {'content': 'Created a script. Published to GitHub. Research done.', 'word_count': 80}
test("Short but action-heavy classified as deep or light",
     classify_tick(short_deep) in ('deep_dive', 'light_activity'),
     f"Got {classify_tick(short_deep)}")

# Spanish stillness
spanish_still = {'content': 'Quietud sostenida. Sin agenda. Nada que agregar. Solo estar presente.', 'word_count': 40}
test("Spanish stillness detected", classify_tick(spanish_still) == 'stillness',
     f"Got {classify_tick(spanish_still)}")

# --- Test parse_duration ---
print("\n⏱️  parse_duration")

tick_with_duration = {'content': 'Stuff happened.\n**Duración:** ~12min\nMore stuff.'}
tick_with_english = {'content': 'Things.\n**Duration:** ~45min'}
tick_no_duration = {'content': 'No duration mentioned here.'}

test("Spanish duration parsed", parse_duration(tick_with_duration) == 12,
     f"Got {parse_duration(tick_with_duration)}")
test("English duration parsed", parse_duration(tick_with_english) == 45,
     f"Got {parse_duration(tick_with_english)}")
test("No duration returns None", parse_duration(tick_no_duration) is None)

# --- Test reflexion counter ---
print("\n🔄 count_reflexions")

# Test with actual file if exists
reflexion_path = Path(os.path.expanduser("~/.openclaw/workspace/memory/reflexions.md"))
if reflexion_path.exists():
    count = count_reflexions()
    test("Reflexions file found and parsed", count >= 0, f"Count: {count}")
    test("Has at least 1 reflexion", count >= 1, f"Count: {count}")
else:
    print("  ⚠️  Skipped — reflexions.md not found")

# --- Test with empty journal ---
print("\n📄 Edge cases")

empty_journal = "# Journal - 2026-01-01\n\nNothing here.\n"
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write(empty_journal)
    tmp_empty = f.name

empty_ticks = parse_journal(tmp_empty)
os.unlink(tmp_empty)
test("Empty journal returns 0 ticks", len(empty_ticks) == 0, f"Got {len(empty_ticks)}")

# Journal with one tick, no separator
single = "# Journal\n\n## 🌅 Tick #1 - 10:00 (Morning)\n\nDid something.\n"
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write(single)
    tmp_single = f.name

single_ticks = parse_journal(tmp_single)
os.unlink(tmp_single)
test("Single tick journal works", len(single_ticks) == 1, f"Got {len(single_ticks)}")

# --- Summary ---
print(f"\n{'=' * 50}")
total = PASS + FAIL
print(f"Results: {PASS}/{total} passed", end="")
if FAIL > 0:
    print(f" — {FAIL} FAILED ❌")
else:
    print(f" — ALL PASSED ✅")
print(f"{'=' * 50}")

sys.exit(1 if FAIL > 0 else 0)
