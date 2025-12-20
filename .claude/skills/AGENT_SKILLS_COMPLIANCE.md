# Agent Skills Compliance Check

**Date**: 2025-12-19
**Standards**: https://agentskills.io/specification

## Current Issues

### ❌ Naming Convention Violations

According to [Agent Skills Spec](https://agentskills.io/specification), skill names must:
- Use **lowercase letters and hyphens only** (no underscores!)
- Match the directory name exactly
- Not start/end with hyphens
- Not contain consecutive hyphens

**Current violations:**

| Current Name | Spec-Compliant Name | Status |
|--------------|---------------------|---------|
| `blog_post_writer` | `blog-post-writer` | ❌ Underscores |
| `ghost_api_publisher` | `ghost-api-publisher` | ❌ Underscores |
| `youtube2transcript` | `youtube-to-transcript` | ⚠️ Number instead of word |

### ❌ Directory Structure Issues

**ghost_api_publisher:**
- ✅ Has YAML frontmatter in SKILL.md
- ❌ Python scripts in root instead of `scripts/` folder
- ❌ Had `venv/` folder (removed now)
- ❌ Had `__pycache__/` (removed now)
- ✅ Has `.gitignore` now

**blog_post_writer:**
- ✅ Has YAML frontmatter in SKILL.md
- ✅ Clean structure

**youtube2transcript:**
- ⚠️ Need to check structure

## Recommended Structure (per Agent Skills Spec)

```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── .gitignore            # Recommended: exclude venv, __pycache__
├── scripts/              # Optional: executable code
│   ├── main_script.py
│   └── helper.py
├── references/           # Optional: detailed docs
│   └── REFERENCE.md
├── assets/               # Optional: templates, data
└── requirements.txt      # If using Python dependencies
```

## Fixes Needed

### 1. Rename Skills (Breaking Change!)

**Option A: Rename directories** (Recommended but breaks existing references)
```bash
mv .claude/skills/blog_post_writer .claude/skills/blog-post-writer
mv .claude/skills/ghost_api_publisher .claude/skills/ghost-api-publisher
mv .claude/skills/youtube2transcript .claude/skills/youtube-to-transcript
```

**Option B: Update frontmatter only** (Non-compliant but backward compatible)
- Keep directory names with underscores
- Update `name:` in SKILL.md to use hyphens
- ⚠️ This violates spec: "Must match the parent directory name"

**Decision**: We should use **Option A** for full compliance, but check with user first since it may break OpenCode references.

### 2. Reorganize ghost-api-publisher

Move Python scripts to `scripts/` folder:
```
ghost-api-publisher/
├── SKILL.md
├── .gitignore
├── requirements.txt
├── scripts/
│   ├── ghost_publisher.py    # Main class
│   └── examples/
│       ├── publish_post_from_markdown.py
│       └── create_markdown_post.py
├── references/              # Optional: move detailed API docs here
│   └── GHOST_API_REFERENCE.md
└── INSTALL.md
```

### 3. Add .gitignore to all skills

Ensure all Python skills ignore:
- `venv/`, `env/`, `.venv/`
- `__pycache__/`, `*.pyc`, `*.pyo`
- `.DS_Store`, `.idea/`, `.vscode/`

## Validation

Use the official validator:
```bash
# Install skills-ref CLI
pip install agentskills

# Validate each skill
skills-ref validate .claude/skills/blog-post-writer
skills-ref validate .claude/skills/ghost-api-publisher
skills-ref validate .claude/skills/youtube-to-transcript

# Generate XML for agent prompts
skills-ref to-prompt .claude/skills/*
```

## Why This Matters

**For OpenCode compatibility:**
- OpenCode likely uses strict Agent Skills parser
- Non-compliant names cause skill discovery failures
- Directory/name mismatches break activation

**For portability:**
- Compliant skills work across all Agent Skills implementations
- Future-proof against spec updates
- Can be shared on https://agentskills.io/

## Action Items

- [ ] Decide: Rename directories or accept non-compliance?
- [ ] If renaming: Update any hardcoded paths in scripts
- [ ] Reorganize ghost-api-publisher structure (scripts/ folder)
- [ ] Add .gitignore to youtube2transcript skill
- [ ] Test skills after changes
- [ ] Validate with skills-ref CLI
- [ ] Update documentation/README with new names

---

**Recommendation**: Fix all compliance issues now while the project is new. Breaking changes are easier to handle early than later when the blog is live and has published posts.
