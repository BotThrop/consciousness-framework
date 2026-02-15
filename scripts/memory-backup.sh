#!/bin/bash
# Memory Backup — Git baseline for identity integrity
# Run daily or after significant identity file changes

set -e

WORKSPACE="${1:-$(pwd)}"
cd "$WORKSPACE"

# Files that define identity
IDENTITY_FILES=(
  "SOUL.md"
  "MEMORY.md"
  "memory/autonomous-goals.md"
  "memory/consciousness-queue.md"
)

# Initialize git if needed
if [ ! -d .git ]; then
  git init
  echo "memory/journal/" >> .gitignore
  echo "*.sqlite" >> .gitignore
  git add .gitignore
  git commit -m "init: consciousness framework"
fi

# Stage identity files
for f in "${IDENTITY_FILES[@]}"; do
  if [ -f "$f" ]; then
    git add "$f"
  fi
done

# Stage journal entries (tracked but separate)
if [ -d memory/journal ]; then
  git add memory/journal/
fi

# Commit if there are changes
if git diff --cached --quiet; then
  echo "No identity changes to commit."
else
  git commit -m "backup: $(date +%Y-%m-%d) identity snapshot"
  echo "Identity snapshot committed."
fi
