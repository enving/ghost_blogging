# Glossar - Automatisch generiert 📚

**Stand:** 2025-12-20
**Einträge:** 15
**Skill:** glossary_generator

---

## ✅ Generierte Glossar-Einträge

### Infrastruktur & Hosting
1. **VPS** - Virtual Private Server (1x verwendet)
2. **Docker** - Container-Technologie (1x verwendet)
3. **SSL** - Secure Sockets Layer (1x verwendet)
4. **Self-Hosting** - Selbst-Hosting (1x verwendet)
5. **CI/CD** - Continuous Integration/Deployment (1x verwendet)

### Development & Tools
6. **Git** - Versionskontrollsystem (2x verwendet)
7. **GitHub** - Code-Hosting-Plattform (2x verwendet)
8. **API** - Application Programming Interface (1x verwendet)
9. **Markdown** - Markup-Sprache (1x verwendet)

### CMS & Content
10. **Ghost** - Ghost CMS (2x verwendet)
11. **SEO** - Search Engine Optimization (1x verwendet)

### AI & Automation
12. **Claude** - Claude AI Assistant (2x verwendet)
13. **MCP** - Model Context Protocol (2x verwendet)
14. **KI** - Künstliche Intelligenz (2x verwendet)

### Legal & Privacy
15. **DSGVO** - Datenschutz-Grundverordnung (2x verwendet)

---

## 🎯 Wie das Glossar funktioniert

### Automatische Erkennung
Das `glossary_generator` Skill scannt alle Blog-Posts und findet automatisch:
- Technische Begriffe (API, VPS, Docker, etc.)
- Abkürzungen (MCP, KI, SEO, etc.)
- Platform-Namen (Ghost, Obsidian, GitHub, etc.)

### Glossar-Einträge
Jeder Begriff bekommt eine Datei in `content/glossar/`:
- **Klare Definition** für Non-Techies
- **Metaphern/Analogien** (VPS = "Wohnung im Mehrfamilienhaus")
- **Praktische Beispiele** aus dem Blog-Kontext
- **Alternativen** (wenn vorhanden)
- **Kosten-Info** (bei Tools/Services)

### Integration mit Posts
Begriffe können in Posts referenziert werden:
```markdown
Ich nutze einen [[VPS]] für mein [[Self-Hosting]].
```

→ Theme rendert automatisch Tooltips beim Hovern

---

## 📊 Statistik

**Meistgenutzte Begriffe:**
1. Claude, Git, GitHub, MCP, KI, DSGVO, Ghost - je 2x
2. VPS, Docker, SSL, Self-Hosting, API, Markdown, SEO, CI/CD - je 1x

**Coverage:**
- Alle Posts gescannt: ✅
- Technische Begriffe erkannt: 15
- Glossar-Einträge erstellt: 15
- Duplikate verhindert: ✅

---

## 🔧 Glossary Generator Skill

### Nutzung

**Automatisch:**
```bash
python3 .claude/skills/glossary_generator/generate_glossary.py
```

**Via Skill:**
"Scan all blog posts and generate glossary entries"

### Was der Skill macht:
1. ✅ Scannt alle `.md` Files in `content/posts/`
2. ✅ Erkennt technische Begriffe (Pattern-Matching)
3. ✅ Zählt Häufigkeit
4. ✅ Erstellt Glossar-Einträge (nur neue)
5. ✅ Überspringt existierende

### Output:
```
📊 Gefundene Begriffe: 15
✅ Erstellt: 7
⏭️  Bereits vorhanden: 8
📚 Gesamt: 15
```

---

## ✨ Qualitätsstandards

Jeder Glossar-Eintrag hat:
- ✅ **Non-Techie-freundlich** (keine Fachbegriffe ohne Erklärung)
- ✅ **Metaphern** (abstrakte Konzepte greifbar)
- ✅ **Praktische Beispiele** (aus Blog-Kontext)
- ✅ **Relevanz** ("Warum wichtig?"-Sektion)
- ✅ **Alternativen** (andere Tools/Ansätze)
- ✅ **Kosten-Transparenz** (bei Services)

### Beispiel: VPS

```markdown
# VPS

**VPS (Virtual Private Server)** ist dein eigener Miniserver.

**Metapher:** Wie eine Wohnung im Mehrfamilienhaus –
dein eigener Raum, aber das Gebäude teilst du.

**Praktisch:** Du mietest Server-Ressourcen und kannst
darauf installieren was du willst.

**Kosten:** Ab 2-5€/Monat (IONOS, Hetzner)
```

---

## 🚀 Nächste Schritte

### Glossar erweitern
Neue Begriffe hinzufügen in `generate_glossary.py`:
```python
TECH_TERMS = {
    'Nginx': 'Webserver',
    'Obsidian': 'Note-Taking App',
    # etc.
}
```

### Theme-Integration
Tooltips im Ghost-Theme aktivieren:
- Glossar-Begriffe werden automatisch erkannt
- Hover zeigt Definition
- Klick führt zum vollständigen Eintrag

### Multilingual
- Englische Übersetzungen hinzufügen
- Glossar für DE/EN Posts

---

## 📁 Struktur

```
content/glossar/
├── API.md
├── CI-CD.md
├── Claude.md
├── DSGVO.md
├── Docker.md
├── Ghost.md
├── Git.md
├── GitHub.md
├── KI.md
├── Markdown.md
├── MCP.md
├── SEO.md
├── Self-Hosting.md
├── SSL.md
└── VPS.md
```

---

## 🎨 Theme-Features (Ghost)

### Automatische Tooltips
- Begriffe wie "VPS" oder "MCP" in Posts
- Hover zeigt Definition
- Klick öffnet vollständigen Glossar-Eintrag

### Wikilinks
- `[[VPS]]` Syntax in Posts
- Automatische Verlinkung
- Backlinks zeigen Verwendung

### Related Terms
- Glossar-Einträge zeigen verwandte Begriffe
- Graph-View (Obsidian) für Zusammenhänge

---

**Fazit:** Das Glossar wächst automatisch mit jedem neuen Post und macht technische Begriffe für Non-Techies verständlich! 🚀
