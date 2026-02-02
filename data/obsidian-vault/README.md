# 🧠 Obsidian Vault - Ghost Blog

Deine lokale Knowledge Base für den Ghost Blog.

## 📁 Struktur

```
obsidian-vault/
├── Posts/              # Blog-Posts
│   ├── published/      # Veröffentlichte Posts
│   └── drafts/         # Entwürfe
├── Glossar/            # Begriffsdefinitionen
├── Templates/          # Vorlagen für Posts
├── Attachments/        # Bilder, PDFs, etc.
└── Ideas/              # Post-Ideen & Notizen
```

## 🚀 Quick Start

### 1. Obsidian installieren

Download: https://obsidian.md/ (kostenlos!)

### 2. Vault öffnen

- Obsidian starten
- "Open folder as vault"
- Diesen Ordner wählen: `ghost_blogging/obsidian-vault`

### 3. Plugins aktivieren (empfohlen)

**Settings → Community Plugins**:

1. **Templates** - Vorlagen nutzen
2. **Dataview** - Queries über Posts
3. **Obsidian Git** - Auto-Backup
4. **Graph Analysis** - Erweiterter Graph

### 4. Ersten Post schreiben

1. Neue Notiz erstellen
2. Strg+T → Template einfügen: "blog-post-template"
3. Ausfüllen & schreiben!

## 🔄 Sync zu Ghost

```bash
# Im Projekt-Root:
python3 obsidian-integration/sync_to_ghost.py

# Erstellt Metadaten in metadata/
# Claude kann dann darauf zugreifen!
```

## 📖 Conventions

### Frontmatter

```yaml
---
title: "Post-Titel"
date: 2025-12-19
tags:
  - KI & Automation
  - Self-Hosting Tutorials
status: draft | published
difficulty: einsteiger | fortgeschritten | expert
reading_time: 10 min
featured: false
related_posts:
  - anderer-post
excerpt: "Kurze Zusammenfassung"
ghost_published: false
ghost_slug: "url-slug"
---
```

### Wikilinks

```markdown
Siehe auch: [[Anderer Post]]
Glossar: [[Glossar/Ghost]]
```

→ Werden automatisch zu Links konvertiert

### Tags

```markdown
Flat:          #KI
Hierarchisch:  #KI/Tools
               #Self-Hosting/VPS
```

## 🎨 Graph View

**Strg+G** → Zeigt Verbindungen zwischen Posts

**Nutzen**:
- Cluster erkennen
- Isolierte Posts finden
- Zusammenhänge visualisieren

## 💡 Tipps

### Dataview Queries

Erstelle Note: "Dashboard.md"

```dataview
TABLE tags, status, reading_time
FROM "Posts"
WHERE status = "draft"
SORT date DESC
```

→ Zeigt alle Drafts

### Templates

Erstelle eigene Templates in `Templates/`:

```markdown
---
title: "{{title}}"
date: {{date}}
---

# {{title}}

Dein Template...
```

### Auto-Sync

Nutze **Obsidian Git** Plugin:

- Settings → Obsidian Git
- Auto-commit: alle 10min
- Push to GitHub: ja

→ Automatisches Backup!

## 🔗 Externe Tools

### Obsidian Publish (optional, kostenpflichtig)

Veröffentliche direkt aus Obsidian:
https://obsidian.md/publish

### Obsidian Sync (optional, kostenpflichtig)

Sync zwischen Geräten:
https://obsidian.md/sync

**Alternative (kostenlos)**:
- Vault in Cloud (Dropbox, OneDrive)
- ODER: Obsidian Git (empfohlen!)

## 📚 Ressourcen

- **Obsidian Docs**: https://help.obsidian.md/
- **Community Plugins**: https://obsidian.md/plugins
- **Forum**: https://forum.obsidian.md/

---

**Happy Writing!** 🚀

*Bei Fragen: Frag Claude!*
