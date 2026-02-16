#!/bin/bash
# Memory Backup — Git baseline for identity integrity
# Run daily or after significant identity file changes

set -e

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    echo ""
    echo "Install git:"
    echo "  • macOS: brew install git"
    echo "  • Ubuntu/Debian: sudo apt-get install git"
    echo "  • Fedora: sudo dnf install git"
    exit 1
fi

WORKSPACE="${1:-$(pwd)}"

if [ ! -d "$WORKSPACE" ]; then
    echo "❌ Error: Workspace directory does not exist: $WORKSPACE"
    exit 1
fi

cd "$WORKSPACE"

echo "🧠 Memory Backup — Identity Integrity"
echo "========================================"
echo "Workspace: $WORKSPACE"
echo ""

# Files that define identity
IDENTITY_FILES=(
  "SOUL.md"
  "MEMORY.md"
  "memory/autonomous-goals.md"
  "memory/consciousness-queue.md"
)

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    
    # Create .gitignore if it doesn't exist
    if [ ! -f .gitignore ]; then
        echo "Creating .gitignore..."
        cat > .gitignore << 'EOF'
# Exclude raw journal entries (can be large)
memory/journal/

# Exclude database files
*.sqlite
*.db

# Exclude system files
.DS_Store
EOF
    fi
    
    git add .gitignore
    
    # Add all existing identity files
    echo "Adding identity files..."
    for f in "${IDENTITY_FILES[@]}"; do
      if [ -f "$f" ]; then
        git add "$f"
        echo "  ✅ $f"
      else
        echo "  ⚠️  $f (not found, skipping)"
      fi
    done
    
    # Add journal entries if they exist
    if [ -d memory/journal ]; then
      # Don't add journal/ to .git tracking by default (it's in .gitignore)
      echo "  ℹ️  memory/journal/ (excluded via .gitignore)"
    fi
    
    # First commit
    if git diff --cached --quiet; then
        echo ""
        echo "⚠️  No files to commit. Initialize your identity files first:"
        echo "  • Create SOUL.md"
        echo "  • Create MEMORY.md"
        echo "  • Or run: bash scripts/install.sh"
        exit 1
    else
        git commit -m "init: consciousness framework — initial identity snapshot"
        echo ""
        echo "✅ Git repository initialized with identity baseline"
        echo ""
        echo "Next steps:"
        echo "  • Add a remote: git remote add origin <url>"
        echo "  • Push to backup: git push -u origin main"
    fi
    
    exit 0
fi

# Git already initialized — proceed with backup
echo "📝 Checking for identity changes..."
echo ""

# Stage identity files
staged_any=false
for f in "${IDENTITY_FILES[@]}"; do
  if [ -f "$f" ]; then
    # Check if file has changes
    if git diff --quiet "$f" && git diff --cached --quiet "$f"; then
      echo "  ⏭️  $f (unchanged)"
    else
      git add "$f"
      echo "  ✅ $f (staged)"
      staged_any=true
    fi
  else
    echo "  ⚠️  $f (not found, skipping)"
  fi
done

# Note: journal entries are excluded via .gitignore
# If you want to track them, remove memory/journal/ from .gitignore

echo ""

# Commit if there are changes
if git diff --cached --quiet; then
  echo "✅ No identity changes to commit."
  echo ""
  echo "Identity files are up to date."
else
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  git commit -m "backup: $timestamp — identity snapshot"
  echo "✅ Identity snapshot committed: $timestamp"
  echo ""
  
  # Show what changed
  echo "Changed files:"
  git diff --name-only HEAD~1 HEAD | sed 's/^/  • /'
  echo ""
  
  # Check if remote is configured
  if git remote | grep -q .; then
    echo "💡 Tip: Push to remote backup with:"
    echo "   git push"
  else
    echo "💡 Tip: Add a remote backup:"
    echo "   git remote add origin <url>"
    echo "   git push -u origin main"
  fi
fi

echo ""
echo "========================================"
echo "Backup complete."
