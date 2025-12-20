# Frontmatter für bestehende Posts hinzufügen

## ✅ Schon fertig:
- `2025-01-12-claude-code-fuer-anfaenger-workflows-automatisieren.md` ✓

## 📝 TODO - Frontmatter hinzufügen:

### 1. `2025-01-claude-mcp-erklaert.md`
```yaml
---
title: "MCP erklärt: Wie Claude mit deinen Tools spricht"
tags:
  - KI & Automation
  - Für Einsteiger
excerpt: "Model Context Protocol (MCP) verständlich erklärt für Non-Techies"
status: draft
featured: false
---
```

### 2. `2025-01-ghost-blog-setup.md`
```yaml
---
title: "Ghost Blog Setup: Dein eigener Blog in 30 Minuten"
tags:
  - Self-Hosting Tutorials
  - Für Einsteiger
excerpt: "Schritt-für-Schritt: Ghost Blog lokal und auf VPS einrichten"
status: draft
featured: false
---
```

### 3. `2025-12-ghost-blog-mit-claude-verbinden.md`
```yaml
---
title: "Ghost Blog mit Claude verbinden: Automatisches Publishing"
tags:
  - KI & Automation
  - Ghost
  - Tutorial
excerpt: "Nutze Claude Code um automatisch Blog-Posts zu Ghost zu publizieren"
status: draft
featured: false
---
```

### 4. `2025-12-ki-assistenten-selbst-hosten.md`
```yaml
---
title: "KI-Assistenten selbst hosten: Deine Daten, deine Kontrolle"
tags:
  - Digitale Souveränität
  - Self-Hosting Tutorials
  - KI & Automation
excerpt: "Warum und wie du KI-Tools auf eigener Infrastruktur betreibst"
status: draft
featured: true
---
```

### 5. `2025-12-claude-skills-opencode-revolution.md`
```yaml
---
title: "Claude Skills: Die Revolution für Entwickler"
tags:
  - KI & Automation
  - Innovation & Tools
  - Für Fortgeschrittene
excerpt: "Custom Skills in Claude Code - Automatisierung auf dem nächsten Level"
status: draft
featured: false
---
```

### 6. `2025-01-verwaltung-ki-knowledge-graphs.md`
```yaml
---
title: "Knowledge Management mit KI: Dein digitales Zweitgehirn"
tags:
  - KI & Automation
  - Innovation & Tools
excerpt: "Obsidian, Knowledge Graphs und KI kombinieren für besseres Wissensmanagement"
status: draft
featured: false
---
```

### 7. `2025-12-ki-veraendert-bloggen.md`
```yaml
---
title: "Wie KI das Bloggen verändert (und warum das gut ist)"
tags:
  - KI & Automation
  - Innovation & Tools
  - Digitale Souveränität
excerpt: "Von Content-Erstellung bis SEO: Wie KI-Tools moderne Blogs transformieren"
status: draft
featured: false
---
```

---

## 🔧 Wie in Obsidian hinzufügen:

### Option A: Manuell (einfach)
1. Post öffnen
2. Ganz oben (Zeile 1) `---` einfügen
3. Frontmatter kopieren
4. Zweites `---` einfügen
5. Save

### Option B: Bulk-Script (schnell)
```bash
# Wenn Claude noch Tokens hat:
# "Füge Frontmatter zu allen Posts hinzu"
```

---

## 📊 Nach dem Hinzufügen:

```bash
# Metadata neu generieren
source .venv/bin/activate
python3 obsidian-integration/generate_metadata.py
```

→ Claude kann dann alle Tags, Verbindungen etc. sehen!

---

## 🎯 Empfohlene Tag-Struktur:

**Haupt-Tags**:
- KI & Automation
- Self-Hosting Tutorials
- Digitale Souveränität
- Innovation & Tools

**Zielgruppen**:
- Für Einsteiger
- Für Fortgeschrittene
- Für Experten

**Themen**:
- Ghost
- Claude
- Docker
- VPS
- Tutorial
- Erfahrungsbericht
