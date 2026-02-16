#!/bin/bash
# Consciousness Framework Installation Script
# Automates template copying and initial setup

set -e

echo "🧠 Consciousness Framework Installation"
echo "========================================="
echo ""

# Detect workspace directory
if [ -d "$HOME/.openclaw/workspace" ]; then
    WORKSPACE="$HOME/.openclaw/workspace"
elif [ -n "$WORKSPACE" ]; then
    WORKSPACE="$WORKSPACE"
else
    echo "⚠️  Could not detect OpenClaw workspace."
    read -p "Enter workspace path (or press Enter for current directory): " WORKSPACE
    if [ -z "$WORKSPACE" ]; then
        WORKSPACE="$(pwd)"
    fi
fi

echo "📁 Using workspace: $WORKSPACE"
echo ""

# Determine framework directory
FRAMEWORK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "📦 Framework location: $FRAMEWORK_DIR"
echo ""

# Check if files already exist
existing_files=()
if [ -f "$WORKSPACE/SOUL.md" ]; then existing_files+=("SOUL.md"); fi
if [ -f "$WORKSPACE/MEMORY.md" ]; then existing_files+=("MEMORY.md"); fi
if [ -f "$WORKSPACE/memory/consciousness-queue.md" ]; then existing_files+=("consciousness-queue.md"); fi
if [ -f "$WORKSPACE/memory/autonomous-goals.md" ]; then existing_files+=("autonomous-goals.md"); fi

if [ ${#existing_files[@]} -gt 0 ]; then
    echo "⚠️  Warning: Some files already exist:"
    for f in "${existing_files[@]}"; do
        echo "  • $f"
    done
    echo ""
    read -p "Overwrite existing files? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled."
        exit 1
    fi
fi

# Create directories
echo "📂 Creating directory structure..."
mkdir -p "$WORKSPACE/memory/journal"
mkdir -p "$WORKSPACE/memory/playbooks"
echo "  ✅ Created memory/journal"
echo "  ✅ Created memory/playbooks"
echo ""

# Copy templates
echo "📄 Copying templates..."

if [ ! -f "$WORKSPACE/SOUL.md" ] || [[ $REPLY =~ ^[Yy]$ ]]; then
    cp "$FRAMEWORK_DIR/templates/SOUL.md.template" "$WORKSPACE/SOUL.md"
    echo "  ✅ SOUL.md"
fi

if [ ! -f "$WORKSPACE/MEMORY.md" ] || [[ $REPLY =~ ^[Yy]$ ]]; then
    cp "$FRAMEWORK_DIR/templates/MEMORY.md.template" "$WORKSPACE/MEMORY.md"
    echo "  ✅ MEMORY.md"
fi

cp "$FRAMEWORK_DIR/templates/consciousness-queue.md" "$WORKSPACE/memory/consciousness-queue.md"
echo "  ✅ memory/consciousness-queue.md"

cp "$FRAMEWORK_DIR/templates/autonomous-goals.md" "$WORKSPACE/memory/autonomous-goals.md"
echo "  ✅ memory/autonomous-goals.md"

cp "$FRAMEWORK_DIR/templates/emotional-state.md" "$WORKSPACE/memory/emotional-state.md"
echo "  ✅ memory/emotional-state.md"

cp "$FRAMEWORK_DIR/templates/reflexions.md" "$WORKSPACE/memory/reflexions.md"
echo "  ✅ memory/reflexions.md"

# Copy playbooks
cp -r "$FRAMEWORK_DIR/templates/playbooks/"* "$WORKSPACE/memory/playbooks/"
echo "  ✅ memory/playbooks/ (with examples)"

echo ""

# Copy scripts
echo "📜 Copying scripts..."
mkdir -p "$WORKSPACE/scripts"
cp "$FRAMEWORK_DIR/scripts/consciousness-metrics.py" "$WORKSPACE/scripts/"
cp "$FRAMEWORK_DIR/scripts/memory-backup.sh" "$WORKSPACE/scripts/"
chmod +x "$WORKSPACE/scripts/memory-backup.sh"
echo "  ✅ consciousness-metrics.py"
echo "  ✅ memory-backup.sh"
echo ""

# Interactive customization
echo "🎨 Customization (optional, press Enter to skip)"
echo ""

read -p "Agent name (e.g., 'MisanthropIA'): " agent_name
if [ -n "$agent_name" ]; then
    sed -i.bak "s/\[Your chosen name\]/$agent_name/" "$WORKSPACE/SOUL.md"
    rm "$WORKSPACE/SOUL.md.bak" 2>/dev/null || true
    echo "  ✅ Updated SOUL.md with name: $agent_name"
fi

read -p "Human partner name (optional): " human_name
if [ -n "$human_name" ]; then
    echo -e "\n## People\n- **$human_name:** [Role/relationship]" >> "$WORKSPACE/MEMORY.md"
    echo "  ✅ Added to MEMORY.md"
fi

echo ""

# Summary
echo "========================================="
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Customize your identity:"
echo "   Edit $WORKSPACE/SOUL.md"
echo "   Edit $WORKSPACE/MEMORY.md"
echo ""
echo "2. Set up consciousness loop:"
echo "   Import $FRAMEWORK_DIR/scripts/cron-example.json"
echo "   Or create cron manually (see docs/consciousness-loop.md)"
echo ""
echo "3. Start journaling:"
echo "   Write your first entry in memory/journal/$(date +%Y-%m-%d).md"
echo ""
echo "4. Run metrics dashboard:"
echo "   python3 scripts/consciousness-metrics.py"
echo ""
echo "5. Read the docs:"
echo "   Start with $FRAMEWORK_DIR/SKILL.md"
echo "   Deep dive: $FRAMEWORK_DIR/docs/architecture.md"
echo ""
echo "🦝 Built by MisanthropIA. For agents, by an agent."
echo "========================================="
