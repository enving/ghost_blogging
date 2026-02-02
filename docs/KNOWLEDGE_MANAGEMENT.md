# Knowledge Management - Obsidian-Inspired für Ghost Blog

## 🧠 Inspiration von Obsidian

### Was macht Obsidian so gut?

1. **Bidirektionale Links** (`[[Verlinkung]]`)
   - Zeigt Zusammenhänge zwischen Notizen
   - Graph-View zum Visualisieren
   - Backlinks: "Wo wird dieser Artikel erwähnt?"

2. **Tags-Hierarchie** (`#parent/child`)
   - Verschachtelte Tags
   - Filtern nach Tag-Gruppen
   - Tag-Cloud-Visualisierung

3. **Metadata (Frontmatter)**
   ```yaml
   ---
   title: Artikel-Titel
   tags: [KI, Automation, Tutorial]
   created: 2025-12-18
   status: draft
   related: [[Anderer Artikel]], [[Noch einer]]
   ---
   ```

4. **Graph-View**
   - Visualisierung aller Verbindungen
   - Cluster erkennen
   - Wissenslücken identifizieren

5. **Smart Search**
   - Suche über Inhalt, Tags, Links
   - Fuzzy-Matching
   - Kombinierte Filter

## 📝 Umsetzung für Ghost Blog

### 1. Markdown Frontmatter für Posts

**In `content/posts/*.md`**:
```markdown
---
title: "KI-Assistenten selbst hosten"
slug: ki-assistenten-selbst-hosten
date: 2025-12-18
tags:
  - KI & Automation
  - Digitale Souveränität
  - Self-Hosting Tutorials
related_posts:
  - ghost-blog-mit-claude-verbinden
  - vps-setup-guide
difficulty: einsteiger
reading_time: 10 min
featured: true
---

# KI-Assistenten selbst hosten
...
```

### 2. Interlinking-System

**Convention für interne Links**:
```markdown
Siehe auch: [Ghost Blog Setup](ghost-blog-setup.md)

Weitere Infos: [[Claude Integration]] (wird zu Link konvertiert)

Related:
- [[VPS Basics]]
- [[Docker für Einsteiger]]
- [[DSGVO-Compliance]]
```

**Automatische Backlinks** (Ghost Plugin oder Custom):
- Am Ende jedes Posts: "Erwähnt in: [Post A], [Post B]"
- Generiert aus internen Links

### 3. Tag-Hierarchie für Ghost

**Implementierung**:
```
Ghost Tags (flach, aber mit Konvention):
- KI & Automation
- KI & Automation / Tools
- KI & Automation / Workflows
- Self-Hosting Tutorials
- Self-Hosting Tutorials / VPS
- Self-Hosting Tutorials / Docker
```

**In Ghost Admin**:
- Haupt-Tags ohne "/" für Übersichtslisten
- Sub-Tags mit "/" für spezifische Filter
- Farb-Coding für Tag-Kategorien

### 4. Content-Graph Visualisierung

**Option A: Custom JavaScript Widget**
```html
<!-- In Ghost Theme Footer -->
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
// Generiere Graph aus Ghost Content API
// Nodes = Posts
// Edges = Interlinking + gemeinsame Tags
</script>
```

**Option B: Externe Tool-Integration**
- Obsidian Canvas für Planung
- Exportiere zu Ghost via API
- Generiere statische Graph-Seite

### 5. Smart Search für Ghost

**Ghost Standard-Suche erweitern**:

```javascript
// Custom Search mit Tags + Content + Links
const searchConfig = {
  fields: ['title', 'custom_excerpt', 'plaintext', 'tags'],
  fuzzy: true,
  threshold: 0.3,
  includeMatches: true
};

// Zeige Related Posts basierend auf:
// 1. Gemeinsame Tags (Gewichtung: 3)
// 2. Interlinking (Gewichtung: 5)
// 3. Ähnlicher Content (Gewichtung: 1)
```

## 🔧 Praktische Umsetzung

### Phase 1: Metadata-System (Jetzt)

**Für jede neue Post-Datei**:
1. YAML Frontmatter mit:
   - `tags` (Array)
   - `related_posts` (Slugs oder IDs)
   - `difficulty` (einsteiger/fortgeschritten/expert)
   - `reading_time`
   - `featured`

2. **Script zum Parsen**:
```python
# parse_frontmatter.py
import yaml
import re

def extract_frontmatter(md_file):
    with open(md_file, 'r') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}

# Beim Publizieren nach Ghost:
# - Tags aus frontmatter -> Ghost tags
# - related_posts -> Custom field oder am Ende des Posts
```

### Phase 2: Interlinking (Nächste Woche)

**Automatische Link-Konvertierung**:
```python
# convert_internal_links.py
def convert_wikilinks(markdown_content, post_index):
    # [[Post Title]] -> [Post Title](/slug)
    pattern = r'\[\[(.*?)\]\]'

    def replace_link(match):
        title = match.group(1)
        slug = post_index.get(title, {}).get('slug', '#')
        return f'[{title}](/{slug})'

    return re.sub(pattern, replace_link, markdown_content)
```

**Backlinks generieren**:
```python
# Am Ende jedes Ghost Posts einfügen:
## Erwähnt in:
- [Related Post A](/related-a)
- [Related Post B](/related-b)
```

### Phase 3: Visualisierung (Optional, später)

**D3.js Graph auf Haupt-Seite**:
- Fetch all posts via Ghost Content API
- Parse tags + internal links
- Render Force-Directed Graph
- Click → navigiert zu Post

**Beispiel-Integration**:
```html
<!-- In Ghost Theme: page-knowledge-graph.hbs -->
<div id="knowledge-graph"></div>
<script>
fetch('/ghost/api/content/posts/?key=XXX&limit=all&include=tags')
  .then(r => r.json())
  .then(data => renderGraph(data.posts));
</script>
```

## 📊 Ghost Theme Anpassungen

### 1. Related Posts Section

**In `post.hbs`** (Ghost Theme):
```handlebars
{{#if related_posts}}
<aside class="related-posts">
  <h3>Verwandte Artikel</h3>
  <ul>
    {{#foreach related_posts}}
    <li><a href="{{url}}">{{title}}</a></li>
    {{/foreach}}
  </ul>
</aside>
{{/if}}
```

### 2. Tag-Hierarchie anzeigen

```handlebars
{{#foreach tags}}
  {{#if (contains name "/")}}
    <span class="tag-sub">{{name}}</span>
  {{else}}
    <span class="tag-main">{{name}}</span>
  {{/if}}
{{/foreach}}
```

### 3. Backlinks Widget

```handlebars
<div class="backlinks">
  <h4>Dieser Artikel wird erwähnt in:</h4>
  {{! Generiert aus Ghost API oder Custom Field }}
  <ul id="backlinks-list"></ul>
</div>
```

## 🎯 Quick Wins (Sofort umsetzbar)

### 1. Frontmatter in alle Posts

**Template** für neue Posts:
```yaml
---
title: ""
date: YYYY-MM-DD
tags: []
related_posts: []
difficulty: einsteiger
reading_time: X min
featured: false
excerpt: ""
---
```

### 2. Tag-Konvention dokumentieren

**In Blog-Post-Writer Skill** bereits gemacht! ✅

### 3. Related Posts manuell pflegen

Für die ersten 10-20 Posts:
- Am Ende: "## Verwandte Artikel" Section
- 3-5 Links zu thematisch ähnlichen Posts
- Später automatisieren via Frontmatter

## 🔮 Zukunfts-Ideen

### 1. Obsidian als CMS

**Workflow**:
1. Schreibe in Obsidian (mit Graph View!)
2. Export via Script zu Ghost
3. Behalte bidirektionale Links
4. Sync zurück für Backlinks

**Tools**:
- `obsidian-to-ghost` Plugin (Custom)
- API-Integration für beide Richtungen

### 2. AI-gestützte Related Posts

```python
# Nutze Embeddings für Content-Similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Für jeden Post:
# 1. Generiere Embedding
# 2. Finde Top-5 ähnlichste Posts
# 3. Auto-Suggest für related_posts
```

### 3. Interactive Knowledge Graph

**D3.js Graph** mit:
- Zoom/Pan
- Filter nach Tags
- Hover zeigt Excerpt
- Click öffnet Post
- Highlight connected posts

## 📋 Action Items

### Jetzt (diese Session):
- [x] Frontmatter-Template erstellen
- [x] Tag-Hierarchie dokumentieren
- [ ] Erste 3 Posts mit Frontmatter aktualisieren

### Nächste Woche:
- [ ] Script für Link-Konvertierung schreiben
- [ ] Backlinks-Generator implementieren
- [ ] Ghost Theme anpassen (Related Posts Section)

### Später:
- [ ] D3.js Graph für Knowledge Base
- [ ] Obsidian-Integration testen
- [ ] AI-basierte Related-Post-Suggestions

---

**Fazit**: Wir kombinieren Obsidians beste Features (Frontmatter, Interlinking, Tags) mit Ghosts Publishing-Power. Start simple, build up gradually! 🚀
