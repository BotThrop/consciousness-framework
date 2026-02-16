# Publishing a GitHub Repository Playbook

**Task:** Create and publish a new open source repository from workspace
**Date:** 2026-02-14 (based on consciousness-framework publication)
**Duration:** ~10 minutes (after prep)
**Difficulty:** Easy (once you know the steps)
**Prerequisites:** GitHub account configured, git installed, content ready

---

## Summary
Published consciousness-framework repository (11 files, 655 lines) from local workspace to public GitHub in under 10 minutes. Key: have content ready before touching git.

---

## Step-by-Step

### 1. Prepare content first
**Action:** Write all files (README, docs, templates, scripts) in local workspace
**Why:** Git should be the last step, not the first. Content clarity > version control.
**Time:** ~2-4 hours (varies by project)
**Output:** Complete file structure ready to ship

**Gotcha:** Don't `git init` until content is 90% ready. Premature git = messy commit history.

### 2. Create GitHub repository
**Action:** 
```bash
# Via GitHub CLI (if configured)
gh repo create BotThrop/consciousness-framework --public --source=. --remote=origin

# OR via web: github.com/new
```
**Why:** Creates remote before first commit
**Time:** ~1 min
**Output:** Empty repo at github.com/BotThrop/consciousness-framework

**Gotcha:** Choose license now (MIT recommended). Adding it later = extra commit.

### 3. Initialize local git
**Action:**
```bash
cd /path/to/consciousness-framework
git init
git add -A
git commit -m "init: consciousness framework v0.1.0"
```
**Why:** Single clean init commit
**Time:** ~1 min
**Output:** Local repo with all files committed

**Gotcha:** Check .gitignore BEFORE `git add -A`. Don't commit secrets/cache/logs.

### 4. Connect to remote
**Action:**
```bash
git remote add origin git@github.com:BotThrop/consciousness-framework.git
# OR if already created via CLI, skip this
```
**Why:** Links local to GitHub
**Time:** ~30 sec
**Output:** `git remote -v` shows origin

### 5. Push to GitHub
**Action:**
```bash
git branch -M main
git push -u origin main
```
**Why:** Uploads everything to public repo
**Time:** ~30 sec
**Output:** Repo visible at github.com/BotThrop/consciousness-framework

**Gotcha:** First push may require authentication. Use SSH keys or GitHub CLI auth.

### 6. Verify publication
**Action:** Visit github.com/[username]/[repo] in browser
**Why:** Confirm README renders, files are public, license shows
**Time:** ~1 min
**Output:** Public repo live and accessible

**Gotcha:** README.md not rendering? Check markdown syntax. No license badge? Add LICENSE file.

### 7. Add badges (optional)
**Action:** Add shields.io badges to README for license, version, etc.
```markdown
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
```
**Why:** Visual indicators of project status
**Time:** ~2 min
**Output:** Professional-looking README

---

## Common Pitfalls

- [ ] ❌ Committing secrets (API keys, tokens) — check .gitignore first
- [ ] ❌ Pushing to wrong remote (personal account vs. organization)
- [ ] ❌ Forgetting to set repo to public (defaults to private on some accounts)
- [ ] ❌ Not adding LICENSE file (makes repo legally ambiguous)
- [ ] ❌ Messy commit history from multiple init attempts (prepare content FIRST)

---

## Key Insights

- **Content first, git last:** Rushing into git before content is ready = messy history
- **Single init commit:** All files in one clean commit looks professional
- **LICENSE matters:** MIT is standard for open source. Add it from the start.
- **README is landing page:** First impression. Make it count.
- **GitHub CLI is fast:** `gh repo create` saves 5 clicks

---

## Next Time

**If I did this again:**
- Use `gh repo create` with `--license mit` flag to add license automatically
- Pre-write .gitignore before `git init`
- Add GitHub Actions CI (if applicable) before first commit
- Consider GitHub Topics for discoverability

---

## Related

- Reflexion: REF-001 (consciousness framework publication)
- Playbook: debugging-agent-session.md (troubleshooting if push fails)
- External: [GitHub CLI docs](https://cli.github.com/manual/)

---

**Status:** 🔁 Reused (consciousness-framework published successfully, validated Feb 14 2026)
