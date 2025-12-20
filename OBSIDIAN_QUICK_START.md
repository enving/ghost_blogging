# 🚀 OBSIDIAN QUICK START - JETZT LOSLEGEN!

## ✅ Was bereits fertig ist:

1. ✅ **Copy-Button für Ghost** → [theme-assets/copy-button/](theme-assets/copy-button/)
2. ✅ **Metadata-System** → [metadata/posts_index.json](metadata/posts_index.json)
3. ✅ **Templates** → [content/posts/Templates/](content/posts/Templates/)
4. ✅ **8 Blog-Posts** → [content/posts/](content/posts/)

---

## 🎯 DEINE NÄCHSTEN SCHRITTE (5 Minuten):

### 1️⃣ Vault öffnen

**In Obsidian**:
- **"Open folder as vault"**
- Wähle: **`/home/enving/Dev/Repositories/ghost_blogging/content/posts`**

### 2️⃣ Send to Ghost Plugin

**Settings → Community plugins → Browse**:
- Suche: **"Send to Ghost"**
- Install → Enable

**Konfiguration**:
- Settings → Send to Ghost
- Ghost URL: `http://localhost:2368` (wenn Ghost läuft)
- Admin API Key: [Siehe unten wie du den holst]

### 3️⃣ Ghost Admin API Key holen

**Falls Ghost lokal läuft**:
1. Browser: http://localhost:2368/ghost
2. Settings → Integrations
3. "+ Add custom integration" → Name: "Obsidian"
4. **Kopiere Admin API Key**
5. In Obsidian einfügen

**Falls Ghost noch nicht läuft**:
→ Arbeite erstmal in Obsidian, Sync später!

### 4️⃣ Templates aktivieren

**Settings → Core plugins**:
- **Templates** ✅ aktivieren
- Template folder: `Templates`

**Nutzen**: Strg+T → Template einfügen

---

## 📝 FRONTMATTER HINZUFÜGEN (20 Minuten)

**Siehe**: [FRONTMATTER_TODO.md](FRONTMATTER_TODO.md)

**Für jeden Post ohne Frontmatter**:

1. Post in Obsidian öffnen
2. Ganz oben (Zeile 1) einfügen:

```yaml
---
title: "Post-Titel"
tags:
  - Tag1
  - Tag2
excerpt: "Kurzbeschreibung"
status: draft
featured: false
---
```

3. Save (Strg+S)

**Oder**: Kopiere Vorschläge aus [FRONTMATTER_TODO.md](FRONTMATTER_TODO.md)!

---

## 🔄 SYNC MIT GHOST

### Test-Post senden:

1. Post in Obsidian öffnen (z.B. claude-code-fuer-anfaenger...)
2. **Strg+P** → "Send to Ghost"
3. Enter!

→ Check Ghost Admin: http://localhost:2368/ghost → Posts

### Metadata aktualisieren (für Claude):

```bash
source .venv/bin/activate
python3 obsidian-integration/generate_metadata.py
```

→ Claude kann dann deine Updates sehen!

---

## 🎨 OBSIDIAN FEATURES NUTZEN

### Graph View (Strg+G)
- Zeigt Verbindungen zwischen Posts
- Nutze `[[Wikilinks]]` in Posts!
- Beispiel: `[[Ghost Blog Setup]]`

### Backlinks
- Rechtes Panel → Backlinks
- Zeigt wo Post erwähnt wird

### Tags
- `#KI` → Filtere Posts nach Tags
- Tag-Pane rechts öffnen

### Quick Switcher (Strg+O)
- Schnell zwischen Posts wechseln

---

## 💡 WORKFLOW AB JETZT

```
1. Obsidian öffnen
2. Neue Notiz (Strg+N)
3. Template (Strg+T)
4. Schreiben...
5. Wikilinks nutzen: [[Anderer Post]]
6. Tags setzen
7. Strg+P → "Send to Ghost"
8. In Ghost Admin reviewen
9. Publish!
```

---

## 🐛 TROUBLESHOOTING

### Plugin findet Ghost nicht
- Prüfe: Ghost läuft? (`ghost ls` im Terminal)
- URL richtig? `http://localhost:2368` (kein Slash am Ende!)

### API Key funktioniert nicht
- Format: `xxx:xxx` (mit Doppelpunkt!)
- In Ghost neu generieren

### Template erscheint nicht
- Settings → Templates → Folder: `Templates` ✓
- Ordner existiert? `/content/posts/Templates`

---

## 📚 HILFREICHE DATEIEN

| Datei | Was ist drin? |
|-------|---------------|
| [FRONTMATTER_TODO.md](FRONTMATTER_TODO.md) | Frontmatter-Vorschläge für alle Posts |
| [.obsidian-vault-config.md](content/posts/.obsidian-vault-config.md) | Detaillierte Setup-Anleitung |
| [SIMPLE_SETUP.md](obsidian-integration/SIMPLE_SETUP.md) | Alternative Setup-Methode |
| [COPY_PASTE_BUTTON.md](COPY_PASTE_BUTTON.md) | Copy-Button Implementierung |

---

## 🤖 CLAUDE NUTZEN

**Frag mich**:
- "Zeige alle Posts mit Tag 'KI'"
- "Schlage Related Posts vor für Post X"
- "Welche Posts haben keine Tags?"
- "Generiere Frontmatter für neue Idee"

**Ich lese**:
- `metadata/posts_index.json` → Alle Posts
- `metadata/links_graph.json` → Verbindungen

**Update Metadata**:
```bash
python3 obsidian-integration/generate_metadata.py
```

---

## ✨ FEATURES DIE JETZT GEHEN

In Obsidian:
- ✅ Alle Posts bearbeiten
- ✅ Graph View
- ✅ Backlinks
- ✅ Templates
- ✅ Send to Ghost

Mit Claude:
- ✅ Metadata-Zugriff
- ✅ Post-Analyse
- ✅ Frontmatter-Generierung
- ✅ Tag-Vorschläge

Auf Ghost (wenn deployed):
- ✅ Copy-Button (aus theme-assets/)
- ✅ Glossar-Tooltips
- ✅ Related Posts
- ✅ Backlinks

---

## 🎯 WICHTIG FÜR SPÄTER

**Wenn du Ghost deployed hast**:

1. Copy-Button aktivieren:
   - Siehe [theme-assets/copy-button/README.md](theme-assets/copy-button/README.md)
   - Quick: Code Injection
   - Oder: Theme Integration

2. Ghost API Key in Obsidian anpassen:
   - Von `http://localhost:2368`
   - Zu `https://deinblog.de`

---

**FERTIG! Du kannst jetzt in Obsidian arbeiten!** 🚀

Bei Fragen: Frag Claude in neuer Session!
