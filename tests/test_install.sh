#!/bin/bash
# Test script for install.sh
# Validates that the installation creates all required files correctly

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEST_DIR="/tmp/consciousness-framework-test-$$"
PASS=0
FAIL=0

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "🧪 INSTALL.SH TEST SUITE"
echo "=========================================="
echo ""

test() {
    local name="$1"
    local condition="$2"
    local detail="${3:-}"
    
    if [ "$condition" = "true" ]; then
        PASS=$((PASS + 1))
        echo -e "${GREEN}✅${NC} $name"
    else
        FAIL=$((FAIL + 1))
        echo -e "${RED}❌${NC} $name${detail:+ — $detail}"
    fi
}

cleanup() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
    fi
}

# Cleanup on exit
trap cleanup EXIT

echo "📁 Test directory: $TEST_DIR"
echo "📦 Framework: $SCRIPT_DIR"
echo ""

# --- Test 1: Clean installation ---
echo "🔧 Test 1: Clean installation"
echo ""

mkdir -p "$TEST_DIR"
cd "$SCRIPT_DIR"

# Run install.sh non-interactively
bash scripts/install.sh "$TEST_DIR" <<EOF 2>&1 > /dev/null


EOF

# Check required directories
test "Created memory/journal/" "$([ -d "$TEST_DIR/memory/journal" ] && echo true || echo false)"
test "Created memory/playbooks/" "$([ -d "$TEST_DIR/memory/playbooks" ] && echo true || echo false)"
test "Created scripts/" "$([ -d "$TEST_DIR/scripts" ] && echo true || echo false)"

# Check required files
test "Created SOUL.md" "$([ -f "$TEST_DIR/SOUL.md" ] && echo true || echo false)"
test "Created MEMORY.md" "$([ -f "$TEST_DIR/MEMORY.md" ] && echo true || echo false)"
test "Created consciousness-queue.md" "$([ -f "$TEST_DIR/memory/consciousness-queue.md" ] && echo true || echo false)"
test "Created autonomous-goals.md" "$([ -f "$TEST_DIR/memory/autonomous-goals.md" ] && echo true || echo false)"
test "Created emotional-state.md" "$([ -f "$TEST_DIR/memory/emotional-state.md" ] && echo true || echo false)"
test "Created reflexions.md" "$([ -f "$TEST_DIR/memory/reflexions.md" ] && echo true || echo false)"

# Check scripts
test "Copied consciousness-metrics.py" "$([ -f "$TEST_DIR/scripts/consciousness-metrics.py" ] && echo true || echo false)"
test "Copied memory-backup.sh" "$([ -f "$TEST_DIR/scripts/memory-backup.sh" ] && echo true || echo false)"
test "memory-backup.sh is executable" "$([ -x "$TEST_DIR/scripts/memory-backup.sh" ] && echo true || echo false)"

# Check playbooks
test "Copied playbooks" "$([ -f "$TEST_DIR/memory/playbooks/README.md" ] && echo true || echo false)"

echo ""

# --- Test 2: File contents validation ---
echo "🔍 Test 2: File contents validation"
echo ""

# Check that SOUL.md has expected content
if grep -q "# SOUL.md - Who I Am" "$TEST_DIR/SOUL.md"; then
    test "SOUL.md has header" "true"
else
    test "SOUL.md has header" "false" "Header not found"
fi

# Check that consciousness-metrics.py is executable Python
if python3 -m py_compile "$TEST_DIR/scripts/consciousness-metrics.py" 2>/dev/null; then
    test "consciousness-metrics.py is valid Python" "true"
else
    test "consciousness-metrics.py is valid Python" "false"
fi

# Check that consciousness-metrics.py has --help
if grep -q "\-\-help" "$TEST_DIR/scripts/consciousness-metrics.py"; then
    test "consciousness-metrics.py has --help flag" "true"
else
    test "consciousness-metrics.py has --help flag" "false"
fi

# Check that memory-backup.sh has git validation
if grep -q "command -v git" "$TEST_DIR/scripts/memory-backup.sh"; then
    test "memory-backup.sh validates git" "true"
else
    test "memory-backup.sh validates git" "false"
fi

echo ""

# --- Test 3: Scripts functionality ---
echo "🚀 Test 3: Scripts functionality"
echo ""

# Test consciousness-metrics.py --help
if cd "$TEST_DIR" && python3 scripts/consciousness-metrics.py --help > /dev/null 2>&1; then
    test "consciousness-metrics.py --help works" "true"
else
    test "consciousness-metrics.py --help works" "false"
fi

# Test consciousness-metrics.py --init
if cd "$TEST_DIR" && python3 scripts/consciousness-metrics.py --init > /dev/null 2>&1; then
    test "consciousness-metrics.py --init works" "true"
else
    test "consciousness-metrics.py --init works" "false"
fi

# Test memory-backup.sh help
if bash "$TEST_DIR/scripts/memory-backup.sh" 2>&1 | grep -q "Memory Backup"; then
    test "memory-backup.sh runs without errors" "true"
else
    test "memory-backup.sh runs without errors" "false"
fi

echo ""

# --- Test 4: File sizes (sanity check) ---
echo "📏 Test 4: File size sanity checks"
echo ""

# SOUL.md should be non-empty and reasonable size
soul_size=$(wc -c < "$TEST_DIR/SOUL.md" | tr -d ' ')
if [ "$soul_size" -gt 100 ] && [ "$soul_size" -lt 10000 ]; then
    test "SOUL.md has reasonable size ($soul_size bytes)" "true"
else
    test "SOUL.md has reasonable size" "false" "$soul_size bytes"
fi

# consciousness-metrics.py should be substantial
metrics_size=$(wc -c < "$TEST_DIR/scripts/consciousness-metrics.py" | tr -d ' ')
if [ "$metrics_size" -gt 5000 ]; then
    test "consciousness-metrics.py is substantial ($metrics_size bytes)" "true"
else
    test "consciousness-metrics.py is substantial" "false" "$metrics_size bytes"
fi

echo ""

# --- Test 5: Environment variable override ---
echo "🌍 Test 5: Environment variable override"
echo ""

TEST_DIR2="/tmp/consciousness-framework-env-test-$$"
mkdir -p "$TEST_DIR2"

WORKSPACE="$TEST_DIR2" bash "$SCRIPT_DIR/scripts/install.sh" <<EOF 2>&1 > /dev/null


EOF

if [ -f "$TEST_DIR2/SOUL.md" ]; then
    test "WORKSPACE env var respected" "true"
else
    test "WORKSPACE env var respected" "false"
fi

rm -rf "$TEST_DIR2"

echo ""

# --- Summary ---
echo "=========================================="
TOTAL=$((PASS + FAIL))
echo "Results: $PASS/$TOTAL passed"

if [ $FAIL -gt 0 ]; then
    echo -e "${RED}$FAIL tests FAILED ❌${NC}"
    echo "=========================================="
    exit 1
else
    echo -e "${GREEN}ALL TESTS PASSED ✅${NC}"
    echo "=========================================="
    exit 0
fi
