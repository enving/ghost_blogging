# Simple Obsidian → Ghost Workflow

## 🎯 Ziel

Posts in Obsidian schreiben → Direkt zu Ghost publishen mit **Send to Ghost** Plugin

## ✅ Was du brauchst

1. **Obsidian** (kostenlos): https://obsidian.md/
2. **Send to Ghost Plugin** (Community Plugin)
3. Dein **Ghost Admin API Key**

---

## 🚀 Setup (5 Minuten)

### 1. Obsidian Vault erstellen

```bash
# Nutze einfach: /home/enving/Dev/Repositories/ghost_blogging/content/posts
# Öffne das in Obsidian als Vault!
```

**In Obsidian**:
- "Open folder as vault"
- Wähle: `/home/enving/Dev/Repositories/ghost_blogging/content/posts`

→ Alle deine Markdown-Posts sind jetzt in Obsidian! ✨

### 2. Send to Ghost Plugin installieren

**In Obsidian**:
1. Settings (⚙️) → Community plugins
2. Browse → Suche "Send to Ghost"
3. Install → Enable

### 3. Ghost API Key holen

**In Ghost Admin** (lokal: http://localhost:2368/ghost):
1. Settings → Integrations
2. "+ Add custom integration"
3. Name: "Obsidian"
4. **Kopiere: Admin API Key** (Format: `xxx:xxx`)

### 4. Plugin konfigurieren

**Obsidian Settings → Send to Ghost**:
- **Ghost URL**: `http://localhost:2368` (oder deine Domain)
- **Admin API Key**: `[dein-key-hier]`
- **Debug**: An (für erste Tests)

---

## 📝 Post schreiben & publishen

### 1. Neue Notiz erstellen

In Obsidian: Neue Notiz in `posts/`

### 2. Frontmatter hinzufügen

```yaml
---
title: "Mein erster Post aus Obsidian"
tags:
  - KI & Automation
  - Tutorial
excerpt: "So publizierst du direkt aus Obsidian zu Ghost"
status: draft
---

# Mein erster Post

Schreib deinen Content hier...

## Section 1

...
```

### 3. Zu Ghost senden

**Strg+P** (Command Palette) → "Send to Ghost"

→ FERTIG! Post ist jetzt in Ghost (als Draft) 🎉

### 4. In Ghost finalisieren

- Öffne Ghost Admin
- Posts → Dein Draft
- Vorschau, letzte Anpassungen
- Publish!

---

## 🎨 Frontmatter-Optionen

```yaml
---
title: "Post-Titel"              # REQUIRED
slug: "url-slug"                 # Optional: Auto-generiert
tags:                            # Optional
  - Tag 1
  - Tag 2
excerpt: "Kurzbeschreibung"      # Optional: Meta-Description
status: draft                    # draft | published
featured: false                  # true = Featured Post
feature_image: "/path/img.jpg"   # Optional: Header-Bild
---
```

---

## 🔄 Workflow-Beispiel

```
1. Idee in Obsidian → Neue Notiz "ideas/meine-idee.md"
2. Outline schreiben
3. Ausarbeiten
4. Verschieben nach "posts/"
5. Frontmatter hinzufügen
6. Strg+P → "Send to Ghost"
7. In Ghost Admin reviewen
8. Publish!
```

---

## 💡 Vorteile

**Obsidian**:
- ✅ Graph View → Verbindungen sehen
- ✅ Backlinks automatisch
- ✅ Schneller Markdown-Editor
- ✅ Offline arbeiten
- ✅ Version Control (Git)

**Ghost**:
- ✅ Professionelles Publishing
- ✅ SEO-Optimierung
- ✅ Newsletter
- ✅ Analytics

**Zusammen**:
- ✅ Beste aus beiden Welten!
- ✅ Knowledge Management + Publishing

---

## 🤖 Claude Integration

**Ich kann auf deine Posts zugreifen**:

```bash
# Einfach Sync-Script laufen lassen:
python3 obsidian-integration/sync_to_ghost.py

# Erstellt metadata/*.json
# Ich kann dann:
# - Alle Posts sehen
# - Verbindungen analysieren
# - Related Posts vorschlagen
# - Lücken finden
```

**Beispiel-Prompt**:
```
"Claude, lies metadata/posts_index.json und zeige mir alle Posts mit Tag 'KI'"

"Schlage 3 neue Posts vor basierend auf vorhandenen"

"Welche Posts haben keine Related Posts?"
```

---

## 📋 Nächste Schritte

1. **Jetzt**: Obsidian installieren & Vault öffnen
2. **Plugin**: Send to Ghost installieren
3. **Test**: Ersten Post publishen
4. **Workflow**: Etablieren

**Bereit?** Lass uns loslegen! 🚀
