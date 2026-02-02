# Obsidian ↔ Ghost Blog Integration

## 🎯 Ziel

**Obsidian als dein lokales Knowledge Management Tool** → Synchronisiert mit Ghost Blog

Du arbeitest in Obsidian (Graph View, Backlinks, etc.), wir (Claude + du) haben immer Zugriff auf alle Metadaten und Verbindungen.

---

## 📐 Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                     DEINE WORKFLOW                           │
└─────────────────────────────────────────────────────────────┘

1. DU schreibst in Obsidian
   ↓
   - Nutzt [[Wikilinks]]
   - Tags mit #tags
   - Frontmatter mit Metadaten
   - Graph View zum Überblick
   ↓

2. SYNC-SCRIPT (automatisch oder on-demand)
   ↓
   - Parsed Obsidian Vault
   - Konvertiert Markdown → Ghost
   - Erstellt Metadaten-Index
   ↓

3. GHOST BLOG (published)
   ↓
   - Posts mit Related/Backlinks
   - Glossar-Page
   - Knowledge Graph
   ↓

4. CLAUDE hat Zugriff auf:
   ↓
   - Metadaten-Index (JSON)
   - Link-Graph
   - Tags-Hierarchie
   → Kann Posts vorschlagen, Links finden, Lücken identifizieren
```

---

## 🗂️ Verzeichnis-Struktur

```
ghost_blogging/
├── obsidian-vault/               # ← Dein Obsidian Vault
│   ├── Posts/                    # Blog-Posts als Markdown
│   │   ├── 2025-01-ghost-setup.md
│   │   ├── 2025-01-claude-integration.md
│   │   └── drafts/               # Entwürfe
│   ├── Glossar/                  # Begriffe
│   │   ├── Ghost.md
│   │   ├── MCP.md
│   │   └── VPS.md
│   ├── Templates/                # Vorlagen
│   │   └── blog-post-template.md
│   └── .obsidian/                # Obsidian Config
│
├── obsidian-integration/         # Sync-Scripts
│   ├── sync_to_ghost.py          # Obsidian → Ghost
│   ├── sync_from_ghost.py        # Ghost → Obsidian (Backlinks)
│   └── generate_metadata.py     # Erstellt Metadaten-Index
│
├── metadata/                     # Für Claude & Scripts
│   ├── posts_index.json          # Alle Posts + Metadaten
│   ├── glossary_index.json       # Alle Glossar-Begriffe
│   ├── links_graph.json          # Link-Verbindungen
│   └── tags_hierarchy.json       # Tag-Struktur
│
└── content/                      # Ghost-Import
    └── posts/                    # Konvertierte Posts
```

---

## 📝 Obsidian Vault Setup

### 1. Obsidian installieren

Download: https://obsidian.md/ (kostenlos!)

### 2. Vault erstellen

```bash
# Erstelle Obsidian Vault im Projekt
mkdir -p /home/enving/Dev/Repositories/ghost_blogging/obsidian-vault
```

In Obsidian:
- "Open folder as vault"
- Wähle `/ghost_blogging/obsidian-vault`

### 3. Folder-Struktur

```
obsidian-vault/
├── Posts/              # Alle Blog-Posts
├── Glossar/            # Definitionen
├── Templates/          # Vorlagen
├── Attachments/        # Bilder, Files
└── Ideas/              # Ideen für Posts
```

---

## 🔧 Post-Template für Obsidian

**File**: `obsidian-vault/Templates/blog-post-template.md`

```markdown
---
title: ""
date: {{date:YYYY-MM-DD}}
tags:
  -
status: draft
difficulty: einsteiger
reading_time:
featured: false
related_posts:
  -
excerpt: ""
ghost_published: false
ghost_slug: ""
---

# {{title}}

## Einleitung

Warum ist dieses Thema wichtig? Was lernt der Leser?

## Hauptteil

### Section 1

...

### Section 2

...

## Fazit

Zusammenfassung + Call-to-Action

---

## Verwandte Artikel

- [[Anderer Post]]
- [[Noch einer]]

## Glossar-Begriffe

Nutze Begriffe aus: [[Glossar/Ghost]], [[Glossar/MCP]], etc.
```

### Template-Nutzung in Obsidian

1. **Obsidian Settings** → Core Plugins → **Templates** aktivieren
2. Template folder: `Templates`
3. Neue Notiz erstellen → Strg+T → Template einfügen

---

## 🔄 Sync-Script: Obsidian → Ghost

**File**: `obsidian-integration/sync_to_ghost.py`

```python
#!/usr/bin/env python3
"""
Obsidian → Ghost Sync Script

Konvertiert Obsidian Markdown-Posts zu Ghost-kompatiblem Format:
- Parsed Frontmatter
- Konvertiert [[Wikilinks]] zu regulären Links
- Erstellt Metadaten-Index
- Uploaded zu Ghost via API
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Ghost API Imports
import requests
import jwt
from time import time

# === KONFIGURATION ===

OBSIDIAN_VAULT = Path("obsidian-vault")
POSTS_DIR = OBSIDIAN_VAULT / "Posts"
GLOSSARY_DIR = OBSIDIAN_VAULT / "Glossar"

METADATA_DIR = Path("metadata")
METADATA_DIR.mkdir(exist_ok=True)

GHOST_URL = os.getenv("GHOST_API_URL", "http://localhost:2368")
GHOST_ADMIN_KEY = os.getenv("GHOST_ADMIN_API_KEY")

# === HELPER FUNCTIONS ===

def extract_frontmatter(md_file: Path) -> tuple[Dict, str]:
    """Extrahiert YAML Frontmatter und Content"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match ---\n...\n---
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2)

    return frontmatter, body


def convert_wikilinks(content: str, posts_index: Dict) -> str:
    """Konvertiert [[Wikilinks]] zu Markdown-Links"""

    def replace_link(match):
        link_text = match.group(1)

        # Suche Post mit diesem Titel
        for slug, post in posts_index.items():
            if post['title'].lower() == link_text.lower():
                return f'[{link_text}](/{slug})'

        # Fallback: Slugify
        slug = slugify(link_text)
        return f'[{link_text}](/{slug})'

    return re.sub(r'\[\[(.*?)\]\]', replace_link, content)


def slugify(text: str) -> str:
    """Konvertiert Text zu URL-Slug"""
    text = text.lower()
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = text.strip('-')
    return text


def generate_posts_index() -> Dict:
    """Scannt Obsidian Vault und erstellt Posts-Index"""

    posts_index = {}

    for md_file in POSTS_DIR.glob("**/*.md"):
        if md_file.parent.name == "drafts":
            continue  # Skip drafts

        frontmatter, body = extract_frontmatter(md_file)

        title = frontmatter.get('title', md_file.stem)
        slug = frontmatter.get('ghost_slug') or slugify(title)

        # Extrahiere interne Links
        wikilinks = re.findall(r'\[\[(.*?)\]\]', body)
        regular_links = re.findall(r'\[.*?\]\((\/.*?)\)', body)

        posts_index[slug] = {
            'title': title,
            'file': str(md_file.relative_to(OBSIDIAN_VAULT)),
            'date': frontmatter.get('date', ''),
            'tags': frontmatter.get('tags', []),
            'status': frontmatter.get('status', 'draft'),
            'difficulty': frontmatter.get('difficulty', 'einsteiger'),
            'reading_time': frontmatter.get('reading_time', ''),
            'featured': frontmatter.get('featured', False),
            'excerpt': frontmatter.get('excerpt', ''),
            'related_posts': frontmatter.get('related_posts', []),
            'wikilinks': wikilinks,
            'internal_links': regular_links,
            'ghost_published': frontmatter.get('ghost_published', False)
        }

    return posts_index


def generate_links_graph(posts_index: Dict) -> Dict:
    """Erstellt Link-Graph für Visualisierung"""

    nodes = []
    edges = []

    for slug, post in posts_index.items():
        nodes.append({
            'id': slug,
            'title': post['title'],
            'tags': post['tags'],
            'status': post['status']
        })

        # Wikilinks → Edges
        for wikilink in post['wikilinks']:
            target_slug = slugify(wikilink)
            if target_slug in posts_index:
                edges.append({
                    'source': slug,
                    'target': target_slug,
                    'type': 'wikilink'
                })

    return {'nodes': nodes, 'edges': edges}


def generate_glossary_index() -> Dict:
    """Scannt Glossar-Ordner und erstellt Index"""

    glossary = {}

    for md_file in GLOSSARY_DIR.glob("*.md"):
        term = md_file.stem
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Erste Zeile als Definition (oder ersten Absatz)
        definition = content.split('\n\n')[0].strip('#').strip()

        glossary[term] = {
            'definition': definition,
            'file': str(md_file.relative_to(OBSIDIAN_VAULT)),
            'url': f'/glossar#{slugify(term)}'
        }

    return glossary


def upload_to_ghost(slug: str, post_data: Dict):
    """Uploaded Post zu Ghost via Admin API"""

    if not GHOST_ADMIN_KEY:
        print("⚠️  GHOST_ADMIN_API_KEY nicht gesetzt. Skip Upload.")
        return

    # Ghost Admin API Token generieren
    key_id, secret = GHOST_ADMIN_KEY.split(':')

    iat = int(time())
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/admin/'
    }

    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

    # Upload Post
    url = f"{GHOST_URL}/ghost/api/admin/posts/"
    headers = {'Authorization': f'Ghost {token}'}

    md_file = OBSIDIAN_VAULT / post_data['file']
    frontmatter, body = extract_frontmatter(md_file)

    # Konvertiere Wikilinks
    posts_index = generate_posts_index()
    body = convert_wikilinks(body, posts_index)

    ghost_post = {
        'posts': [{
            'title': post_data['title'],
            'slug': slug,
            'mobiledoc': json.dumps({  # Oder nutze 'html'
                'version': '0.3.1',
                'markups': [],
                'atoms': [],
                'cards': [['markdown', {'markdown': body}]],
                'sections': [[10, 0]]
            }),
            'status': 'draft' if post_data['status'] == 'draft' else 'published',
            'tags': [{'name': tag} for tag in post_data['tags']],
            'custom_excerpt': post_data['excerpt'],
            'featured': post_data['featured']
        }]
    }

    response = requests.post(url, json=ghost_post, headers=headers)

    if response.ok:
        print(f"✅ {slug} uploaded to Ghost")
    else:
        print(f"❌ {slug} upload failed: {response.text}")


# === MAIN FUNCTION ===

def main():
    print("🔄 Obsidian → Ghost Sync\n")

    # 1. Generate Posts Index
    print("📊 Generating Posts Index...")
    posts_index = generate_posts_index()
    with open(METADATA_DIR / "posts_index.json", 'w') as f:
        json.dump(posts_index, f, indent=2, ensure_ascii=False)
    print(f"   → {len(posts_index)} posts indexed\n")

    # 2. Generate Links Graph
    print("🕸️  Generating Links Graph...")
    links_graph = generate_links_graph(posts_index)
    with open(METADATA_DIR / "links_graph.json", 'w') as f:
        json.dump(links_graph, f, indent=2, ensure_ascii=False)
    print(f"   → {len(links_graph['nodes'])} nodes, {len(links_graph['edges'])} edges\n")

    # 3. Generate Glossary Index
    print("📖 Generating Glossary Index...")
    glossary = generate_glossary_index()
    with open(METADATA_DIR / "glossary_index.json", 'w') as f:
        json.dump(glossary, f, indent=2, ensure_ascii=False)
    print(f"   → {len(glossary)} terms indexed\n")

    # 4. Upload zu Ghost (optional)
    upload = input("Upload to Ghost? (y/n): ").lower() == 'y'
    if upload:
        print("\n📤 Uploading to Ghost...")
        for slug, post in posts_index.items():
            if post['status'] != 'draft':  # Nur published
                upload_to_ghost(slug, post)

    print("\n✅ Sync complete!")
    print(f"   Metadata saved to: {METADATA_DIR}/")


if __name__ == "__main__":
    main()
```

---

## 🔍 Claude Integration

**So kann ich (Claude) auf deine Metadaten zugreifen**:

```python
# In jedem Chat kann ich:
metadata = read_file("metadata/posts_index.json")
links = read_file("metadata/links_graph.json")
glossary = read_file("metadata/glossary_index.json")

# Dann kann ich:
# - Posts mit bestimmten Tags finden
# - Related Posts vorschlagen
# - Lücken im Knowledge Graph identifizieren
# - Glossar-Begriffe vorschlagen
# - Backlinks finden
```

**Beispiel-Prompts für dich**:

```
"Welche Posts haben Tag 'KI' aber fehlen Link zu 'Claude'?"

"Zeige mir alle Posts die auf 'VPS Setup' verlinken"

"Welche Glossar-Begriffe fehlen noch Definitionen?"

"Schlage 3 neue Post-Ideen vor basierend auf vorhandenen Posts"
```

---

## 🚀 Workflow-Beispiel

### Szenario: Neuer Blog-Post schreiben

```
1. DU in Obsidian:
   - Neue Notiz aus Template
   - Schreibst Post mit [[Wikilinks]]
   - Siehst Graph View → Verbindungen
   - Tags setzen

2. Sync ausführen:
   python obsidian-integration/sync_to_ghost.py

3. Claude hat Zugriff:
   - Liest metadata/posts_index.json
   - Sieht neue Verbindungen
   - Kann Related Posts vorschlagen

4. Upload zu Ghost:
   - Automatisch via Script
   - Oder manuell via Ghost Admin
```

---

## 📊 Obsidian Plugins (Empfohlen)

### Must-Have Plugins:

1. **Dataview** - Queries über deine Notes
   ```dataview
   TABLE tags, status
   FROM "Posts"
   WHERE status = "draft"
   ```

2. **Templater** - Erweiterte Templates
   ```
   Automatisch: Datum, Slug-Generierung
   ```

3. **Obsidian Git** - Auto-Backup zu GitHub
   ```
   Automatisch: Commit + Push alle 10min
   ```

4. **Tag Wrangler** - Tag-Management

5. **Graph Analysis** - Erweiterte Graph-View

---

## 🎨 Obsidian Graph View

**So nutzt du es**:

1. Strg+G → Öffnet Graph
2. Suchfilter: `tag:#KI`
3. Färbung nach Tags/Folders
4. Identifiziere Cluster & Lücken

**Was du siehst**:
- Alle Posts als Nodes
- [[Wikilinks]] als Verbindungen
- Isolierte Posts = Potenzial für Interlinking

---

## 📋 Nächste Schritte

### Jetzt sofort:

1. **Obsidian installieren**
   ```bash
   # Download: https://obsidian.md
   ```

2. **Vault erstellen**
   ```bash
   mkdir -p obsidian-vault/{Posts,Glossar,Templates,Attachments,Ideas}
   ```

3. **Template anlegen**
   - Nutze Template oben
   - Speichere in `Templates/blog-post-template.md`

4. **Ersten Post schreiben**
   - In Obsidian: Neue Notiz → Template einfügen
   - Schreib deinen ersten Post!

5. **Sync-Script testen**
   ```bash
   python3 obsidian-integration/sync_to_ghost.py
   # Prüfe: metadata/posts_index.json
   ```

---

## 🔮 Future Features

- [ ] **Obsidian Publish** → Direkt zu Ghost
- [ ] **Bi-direktionales Sync** (Ghost → Obsidian Backlinks)
- [ ] **AI-Suggestions** in Obsidian (via Claude Plugin)
- [ ] **Knowledge Graph** auf Ghost-Blog
- [ ] **Automatisches Tagging** via AI

---

**Bereit loszulegen?** Sag mir wenn du Obsidian installiert hast, dann erstelle ich dir die initialen Files! 🚀
