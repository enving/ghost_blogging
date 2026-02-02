# Copy Button + Knowledge Management Integration

Anthropic-inspirierter Copy-Button mit erweitertem Knowledge Management für Ghost Blog.

## 🎯 Features

### ✅ Basis-Features
- **Copy-to-Clipboard Button** (wie bei Claude.ai)
- Extrahiert Artikel als Markdown
- Preserviert Formatierung (Code, Listen, etc.)
- Dark Mode Support

### 🚀 Enhanced Features
- **Glossar-Tooltips**: Automatische Definitionen für Fachbegriffe
- **Wikilinks**: `[[Begriff]]` → automatische interne Links
- **Related Posts**: Basierend auf gemeinsamen Tags
- **Backlinks**: Zeigt an, welche Posts hierher verlinken
- **Knowledge Graph**: (Optional) Visualisierung aller Verbindungen

---

## 📦 Installation

### Variante 1: Quick Start (Code Injection)

**Schnellste Methode - Keine Theme-Änderungen nötig**

1. Öffne Ghost Admin → Settings → Code Injection
2. Füge in **Site Footer** ein:

```html
<!-- Copy Button + Enhanced Features -->
<link rel="stylesheet" href="https://YOUR-DOMAIN/assets/enhanced-copy.css">
<script src="https://YOUR-DOMAIN/assets/enhanced-copy.js" defer></script>
```

3. Kopiere die Dateien:
   - `04-enhanced-with-glossary.js` → Upload als `enhanced-copy.js`
   - `05-enhanced-styles.css` → Upload als `enhanced-copy.css`

4. **Wichtig**: Setze deinen Ghost Content API Key in `enhanced-copy.js` (Zeile 29)

---

### Variante 2: Theme-Integration (Empfohlen)

**Für vollständige Kontrolle und Performance**

#### Schritt 1: Dateien ins Theme kopieren

```bash
# Theme-Struktur
content/themes/dein-theme/
├── assets/
│   ├── css/
│   │   └── enhanced-copy.css     # ← 05-enhanced-styles.css
│   └── js/
│       └── enhanced-copy.js      # ← 04-enhanced-with-glossary.js
└── default.hbs
```

#### Schritt 2: In `default.hbs` einbinden

**Im `<head>`-Bereich**:
```handlebars
<link rel="stylesheet" href="{{asset "css/enhanced-copy.css"}}">
```

**Vor `</body>`**:
```handlebars
<script src="{{asset "js/enhanced-copy.js"}}" defer></script>
```

#### Schritt 3: Ghost Content API Key setzen

1. Ghost Admin → Settings → Integrations
2. "Add custom integration" → Name: "Knowledge Management"
3. Kopiere **Content API Key** (Public key, safe to expose)
4. In `enhanced-copy.js` Zeile 29 einfügen:

```javascript
ghostApiKey: 'dein_content_api_key_hier',
```

#### Schritt 4: Theme neu starten

```bash
ghost restart
```

---

### Variante 3: Nur Copy Button (Minimal)

Falls du NUR den Copy-Button ohne Knowledge-Features willst:

**Nutze**: `01-code-injection-simple.html`

Ghost Admin → Code Injection → Site Footer → Kompletten Code einfügen

---

## ⚙️ Konfiguration

### Features aktivieren/deaktivieren

In `enhanced-copy.js` (Zeile 35-41):

```javascript
features: {
  copyButton: true,        // Copy-Button anzeigen
  glossaryTooltips: true,  // Glossar-Tooltips aktivieren
  wikilinks: true,         // [[Links]] konvertieren
  relatedPosts: true,      // Related Posts anzeigen
  backlinks: true,         // Backlinks anzeigen
  knowledgeGraph: false    // Knowledge Graph (später)
}
```

### Glossar erweitern

**Option A: Direkt in JavaScript (einfach)**

In `enhanced-copy.js` (Zeile 15-31):

```javascript
glossary: {
  'Neuer Begriff': {
    definition: 'Erklärung des Begriffs',
    url: '/glossar/neuer-begriff'
  },
  // Weitere Begriffe...
}
```

**Option B: Aus Ghost-Seite laden (empfohlen)**

1. Erstelle neue Ghost-Seite: **Slug: `glossar`**
2. Nutze folgendes Format:

```html
<dl>
  <dt>Ghost</dt>
  <dd>Open-Source Blogging-Plattform, fokussiert auf Publishing.</dd>

  <dt>MCP</dt>
  <dd>Model Context Protocol - Schnittstelle zwischen KI und Tools.</dd>

  <dt>VPS</dt>
  <dd>Virtual Private Server - Virtueller dedizierter Server.</dd>
</dl>
```

3. Script lädt automatisch beim Seitenaufruf!

### UI-Texte anpassen

In `enhanced-copy.js` (Zeile 54-60):

```javascript
text: {
  copyButton: 'Artikel kopieren',  // Button-Text
  copied: '✓ Kopiert!',            // Success-Message
  error: '❌ Fehler',               // Error-Message
  relatedPosts: 'Verwandte Artikel',
  backlinks: 'Erwähnt in',
  glossary: 'Glossar'
}
```

---

## 🎨 Styling anpassen

### Farben ändern

In `enhanced-copy.css`:

```css
/* Copy Button Farbe */
.copy-article-btn {
  border-color: rgba(0, 0, 0, 0.12);  /* ← Anpassen */
  color: rgba(0, 0, 0, 0.7);
}

/* Success-State Farbe */
.copy-article-btn.copied {
  background: rgba(16, 185, 129, 0.1);  /* ← Grün */
  color: #10b981;
}

/* Related Posts Highlight */
.related-posts-section {
  background: rgba(0, 123, 255, 0.03);  /* ← Blau */
  border-left-color: #007bff;
}
```

### Position anpassen

```css
/* Copy Button Position */
.copy-article-container {
  text-align: center;  /* left, right, center */
  margin: 3rem auto 2rem;  /* Abstände anpassen */
}
```

---

## 📝 Usage Guide

### 1. Glossar-Begriffe verwenden

Schreibe einfach den Begriff im Text:

```markdown
**Ghost** ist eine Blogging-Plattform.
Ein **VPS** ermöglicht **Self-Hosting**.
```

→ Automatisch werden Tooltips hinzugefügt!

### 2. Wikilinks nutzen

```markdown
Mehr Infos: [[Claude Integration]]
Siehe auch: [[Docker Basics]] und [[VPS Setup]]
```

→ Konvertiert zu:
```html
<a href="/claude-integration" class="wikilink">Claude Integration</a>
```

### 3. Related Posts automatisch

Tags in Ghost setzen:
- Post A: Tags = ["KI", "Automation"]
- Post B: Tags = ["KI", "Tools"]

→ Post A zeigt automatisch Post B in "Verwandte Artikel"

### 4. Backlinks generieren

Verlinke in Post A zu Post B:

```markdown
Siehe [Mein anderer Post](/anderer-post)
```

→ Post B zeigt automatisch: "Erwähnt in: Mein anderer Post"

---

## 🔧 Troubleshooting

### Copy Button erscheint nicht

**Prüfen**:
1. Script geladen? → Browser DevTools → Network Tab
2. Fehler in Console? → Browser DevTools → Console
3. Content-Selektor richtig? → Prüfe `CONFIG.selectors.content`

**Lösung**:
```javascript
// In enhanced-copy.js anpassen:
selectors: {
  content: ['.dein-theme-class', '.gh-content'],  // ← Theme-spezifisch
  // ...
}
```

### Glossar-Tooltips funktionieren nicht

**Prüfen**:
1. Ist `glossaryTooltips: true`?
2. Begriff exakt wie in Config? (Case-sensitive!)
3. CSS geladen?

**Lösung**:
```javascript
// Begriff hinzufügen:
glossary: {
  'Begriff': {  // ← Exakt wie im Text (Groß-/Kleinschreibung!)
    definition: 'Definition',
    url: '/glossar/begriff'
  }
}
```

### Related Posts werden nicht geladen

**Prüfen**:
1. Content API Key gesetzt?
2. API-Key korrekt?
3. Browser Console → Fehler?

**Testen**:
```javascript
// In Browser Console:
fetch('https://deinblog.de/ghost/api/content/posts/?key=DEIN_KEY&limit=1')
  .then(r => r.json())
  .then(console.log);

// Sollte Posts zurückgeben
```

### Performance-Probleme

**Optimierungen**:

```javascript
// Lazy-Load für Related Posts
features: {
  relatedPosts: false,  // Deaktivieren
}

// Oder nur auf Klick laden:
// → Custom Implementation nötig
```

---

## 📚 Erweiterte Features

### Knowledge Graph (Coming Soon)

**Aktivieren** (wenn bereit):
```javascript
features: {
  knowledgeGraph: true
}
```

**Erstelle Seite**: `page-knowledge-graph.hbs`

```html
<div id="knowledge-graph" style="width: 100%; height: 600px;"></div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="{{asset "js/knowledge-graph.js"}}"></script>
```

### Custom Markdown-Export

**Erweitere** `extractArticleAsMarkdown()`:

```javascript
// Füge Custom-Metadaten hinzu
function extractArticleAsMarkdown() {
  let md = '---\n';
  md += 'exported: ' + new Date().toISOString() + '\n';
  md += 'source: ' + window.location.href + '\n';
  md += '---\n\n';

  // ... Rest wie bisher
}
```

---

## 🎯 Best Practices

### Glossar pflegen

1. **Zentrale Glossar-Seite** erstellen (`/glossar`)
2. Begriffe alphabetisch sortieren
3. Kurze Definitionen (1-2 Sätze)
4. Links zu ausführlichen Posts

### Interlinking-Strategie

1. **Wikilinks** für interne Konzepte
2. **Related Posts** automatisch durch Tags
3. **Backlinks** zeigen Verbindungen
4. **Manuelle Links** in Text für Kontext

### Tag-Hierarchie

```
Haupt-Tags (flach):
- KI & Automation
- Self-Hosting Tutorials
- Digitale Souveränität

Sub-Tags (mit /):
- KI & Automation / Tools
- KI & Automation / Workflows
- Self-Hosting Tutorials / VPS
- Self-Hosting Tutorials / Docker
```

---

## 📊 Analytics & Monitoring

### Track Copy-Events (optional)

```javascript
// In enhanced-copy.js nach successful copy:
if (window.plausible) {
  plausible('Article Copied', {
    props: { slug: getCurrentPostSlug() }
  });
}
```

### Monitor API-Calls

```javascript
// In Browser DevTools → Network:
// Filter: "ghost/api"
// → Prüfe Related Posts & Backlinks Requests
```

---

## 🚀 Roadmap

- [x] Copy-to-Clipboard Button
- [x] Markdown-Extraktion
- [x] Glossar-Tooltips
- [x] Wikilinks-Support
- [x] Related Posts
- [x] Backlinks
- [ ] Knowledge Graph Visualisierung
- [ ] Obsidian Sync
- [ ] AI-basierte Related Posts
- [ ] Export-Formate (PDF, EPUB)

---

## 📄 Dateien-Übersicht

| Datei | Beschreibung | Empfohlen für |
|-------|--------------|---------------|
| `01-code-injection-simple.html` | Nur Copy Button, keine Dependencies | Quick Start |
| `02-standalone-script.js` | Copy Button mit besserer Markdown-Extraktion | Basis-Integration |
| `03-styles.css` | Basis-Styles für Copy Button | Mit 02 nutzen |
| `04-enhanced-with-glossary.js` | **Full Featured Script** | Production |
| `05-enhanced-styles.css` | **Full Featured Styles** | Production |
| `README.md` | Diese Anleitung | Dokumentation |

---

## 🤝 Contributing

Verbesserungen? Issues? Ideen?

→ Öffne Issue oder Pull Request im Ghost-Blog Repo

---

## 📜 License

MIT License - Frei nutzbar für deinen Ghost Blog

---

**Erstellt für**: Digitalalchemisten Blog
**Inspiration**: Anthropic Claude.ai + Obsidian.md
**Version**: 1.0
**Datum**: 2025-12-19
