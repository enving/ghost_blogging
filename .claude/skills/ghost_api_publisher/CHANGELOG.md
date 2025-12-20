# Ghost API Publisher - Changelog

## [2.0.0] - 2025-12-19

### 🔴 BREAKING CHANGES

**Ghost v5+ now uses Lexical format instead of HTML!**

#### Changed Method Signatures

**create_post():**
- ❌ OLD: `html_content: str`
- ✅ NEW: `markdown_content: str`
- Added: `featured: bool = False`
- Added: `visibility: str = "public"`

**update_post():**
- ❌ OLD: `html_content: Optional[str]`
- ✅ NEW: `markdown_content: Optional[str]`
- Added: `featured: Optional[bool]`
- Added: `visibility: Optional[str]`

### ✅ Fixed Issues

1. **Posts only showing title** → Fixed by using Lexical format
2. **HTML deprecation** → Now uses Markdown → Lexical conversion
3. **Missing featured/visibility fields** → Added to both methods

### Migration Guide

**Before (broken with Ghost v5+):**
```python
publisher.create_post(
    title="My Post",
    html_content="<p>HTML content</p>",  # ❌ Deprecated!
    status="draft"
)
```

**After (Ghost v5+ compatible):**
```python
publisher.create_post(
    title="My Post",
    markdown_content="# My Markdown\n\nContent here",  # ✅ Correct!
    status="draft",
    featured=True,  # NEW: Feature on homepage
    visibility="public"  # NEW: public/members/paid
)
```

### How it Works

The `markdown_content` is automatically converted to Ghost's Lexical format:

```json
{
  "root": {
    "children": [{
      "type": "markdown",
      "version": 1,
      "markdown": "your markdown content here"
    }],
    "direction": "ltr",
    "format": "",
    "indent": 0,
    "type": "root",
    "version": 1
  }
}
```

This is then serialized as JSON and sent in the `lexical` field (not `html`!).

### Why This Change?

Ghost v5 deprecated the `html` field in favor of `lexical` (their new editor format).
Using the old `html` field results in posts that only show the title with no content.

### Compatibility

- ✅ Ghost v5.0+
- ✅ Markdown input
- ✅ Featured posts
- ✅ Visibility settings (public/members/paid)
- ❌ Ghost v4.x (use v1.x of this skill)

---

## [1.0.0] - 2025-12-18

### Initial Release

- Basic Ghost Admin API integration
- JWT authentication
- HTML-based post creation (now deprecated)
- CRUD operations for posts
