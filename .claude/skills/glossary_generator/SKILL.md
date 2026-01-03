---
name: glossary_generator
description: Automatically extracts technical terms from blog posts and creates/updates glossary entries. Maintains a comprehensive glossary for all technical concepts used across the blog.
---

# Glossary Generator Skill

## Purpose

Automatically identify technical terms, abbreviations, and concepts in blog posts and create comprehensive glossary entries that explain them for non-technical readers.

## How It Works

1. **Term Detection**: Scans all `.md` files in `content/posts/` for technical terms
2. **Frequency Analysis**: Counts how often each term appears
3. **Auto-Generation**: Creates glossary entries in `content/glossar/` with:
   - Clear definition for non-techies
   - Practical examples
   - Related terms
   - Alternatives (if applicable)

## Capabilities

- ✅ Extract technical terms from markdown files
- ✅ Recognize abbreviations (API, VPS, DSGVO, etc.)
- ✅ Create new glossary entries automatically
- ✅ Skip existing entries (no duplication)
- ✅ Sort by frequency (most used terms first)
- ✅ Safe filename handling (CI/CD → CI-CD.md)

## Term Categories

### Infrastructure & Hosting
- VPS, Docker, SSH, SSL, Nginx, MySQL
- Self-Hosting, CI/CD

### Development & Tools
- Git, GitHub, API, Node.js, Python
- Markdown, YAML, JSON, JWT

### CMS & Content
- Ghost, Obsidian, Wikilinks, Frontmatter, SEO

### AI & Automation
- Claude, MCP, KI, AI, LLM

### Legal & Privacy
- DSGVO, Open Source

## Glossary Entry Structure

Each entry (`content/glossar/{Term}.md`) contains:

```markdown
# {Term}

**{Term} ({Full Name})** ist {kurze Erklärung}.

**Einfach erklärt:** {Metapher oder Analogie}

**Praktisch bedeutet das:** {Konkrete Anwendung}

**Beispiel:** {Real-world use case}

**Warum wichtig:** {Relevanz für Zielgruppe}

**Alternative:** {Andere Optionen, falls vorhanden}

---

**Kategorie:** Glossar
**Verwandt mit:** {Related topics}
```

## Usage Examples

### Automatic Generation from Posts

"Scan all blog posts and generate glossary entries for any technical terms"

→ Script finds terms like "VPS", "Ghost", "MCP" and creates comprehensive entries

### Update Existing Glossary

"Check if there are new technical terms in recent posts and add them to the glossary"

→ Only creates entries for new terms, skips existing ones

### List Most Used Terms

"Show me which technical terms are most frequently used across all posts"

→ Frequency analysis helps prioritize which terms need the best explanations

## Target Audience Considerations

**Zielgruppe:** Non-Techies (CEOs, Quereinsteiger, Wissbegierige)

**Schreibstil für Glossar:**
- ✅ Metaphern & Analogien (VPS = "Wohnung im Mehrfamilienhaus")
- ✅ Praktische Beispiele (nicht nur Theorie)
- ✅ "Warum wichtig?"-Sektion (Relevanz zeigen)
- ✅ Alternativen nennen (Obsidian vs. Notion)
- ❌ Fachjargon ohne Erklärung
- ❌ Zu technische Details
- ❌ Annahmen von Vorkenntnissen

## Integration with Blog Posts

### Automatic Tooltips (Theme Feature)

Begriffe wie `[[MCP]]` oder `[[VPS]]` werden automatisch zu Tooltips:
- Beim Hovern erscheint die Definition
- Klick führt zum vollständigen Glossar-Eintrag
- Wikilink-Syntax wird vom Theme erkannt

### Manual Inline References

In Posts können Glossar-Begriffe manuell referenziert werden:

```markdown
Ich nutze einen [[VPS]] in Deutschland für mein Self-Hosting.
```

→ Theme rendert dies als Link zum Glossar-Eintrag mit Hover-Tooltip

## Script Location

**Main Script:** `generate_glossary.py` (root directory)

**Output:** `content/glossar/*.md`

## Maintenance

### Adding New Terms

Edit `TECH_TERMS` dictionary in `generate_glossary.py`:

```python
TECH_TERMS = {
    'NeuerBegriff': 'Vollständiger Name',
    # ...
}
```

Then add definition to `GLOSSAR_DEFINITIONS`:

```python
GLOSSAR_DEFINITIONS = {
    'NeuerBegriff': """**NeuerBegriff** ist...

    **Einfach erklärt:**...
    """,
}
```

### Running the Script

```bash
python3 generate_glossary.py
```

**Output:**
- Shows found terms and frequency
- Creates missing glossary entries
- Skips existing entries
- Summary statistics

## Quality Standards

### Good Glossary Entry Example

```markdown
# VPS

**VPS (Virtual Private Server)** ist dein eigener Miniserver in einem Rechenzentrum.

**Metapher:** Wie eine Wohnung in einem Mehrfamilienhaus – dein eigener Raum, aber das Gebäude teilst du.

**Praktisch:** Du mietest Server-Ressourcen (CPU, RAM, Speicher) und kannst darauf installieren was du willst.

**Kosten:** Ab 2-5€/Monat (z.B. IONOS, Hetzner)

**Warum wichtig:** Für Self-Hosting deines Ghost-Blogs brauchst du einen VPS.

**Alternative:** Shared Hosting (günstiger, weniger Kontrolle)
```

### Bad Example (Too Technical)

```markdown
# VPS

A VPS is a virtualized server instance allocated within a physical server via hypervisor technology, providing dedicated resource allocation...
```

❌ **Problem:** Zu technisch, keine Analogie, keine praktische Relevanz

## Best Practices

1. **Non-Techie First**: Immer für absolute Anfänger schreiben
2. **Metaphern nutzen**: Abstrakte Konzepte greifbar machen
3. **Praxis-Fokus**: "Was bedeutet das für mich als Blogger?"
4. **Kosten transparent**: Bei Tools/Services immer Preise nennen
5. **Alternativen**: Nie nur eine Option zeigen
6. **Kurz & prägnant**: 3-5 Absätze reichen

## Future Enhancements

- [ ] Auto-detect new terms from external sources (docs, articles)
- [ ] Multilingual support (EN/DE)
- [ ] Glossary search functionality
- [ ] Related terms auto-linking
- [ ] Usage statistics per term

## Dependencies

**Python Libraries:**
- `pathlib` (standard library)
- `re` (standard library)
- `collections` (standard library)

**No external dependencies!**

## Error Handling

- Filename sanitization for terms with special characters (CI/CD → CI-CD.md)
- Graceful handling of missing posts directory
- Skip non-markdown files automatically
- No duplication of existing entries

---

**Last Updated:** 2025-12-20
**Version:** 1.0
**Status:** Production Ready

## Example Workflow

```python
# User asks: "Are there any technical terms in my posts that need explanation?"

# Skill executes:
1. Scan content/posts/*.md
2. Find technical terms (API, VPS, Ghost, etc.)
3. Generate glossary entries for new terms
4. Report: "Created 7 new entries, 8 already existed"

# Result: Comprehensive glossary with 15+ entries
```

---

**Integration:** Works seamlessly with Blog-Post-Writer skill – technical terms used in posts are automatically documented in the glossary.
