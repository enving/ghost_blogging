---
title: Warum Obsidian perfekt für Blogger ist
tags:
  - Innovation & Tools
  - Für Einsteiger
  - Ghost
excerpt: "Notiz-App trifft Blog-Redaktion: Wie Obsidian dein Content-Chaos in ein vernetztes Wissenssystem verwandelt – ohne Cloud-Zwang."
status: draft
featured: false
---

# Warum Obsidian perfekt für Blogger ist

Letzte Woche habe ich meine Blog-Redaktion komplett umgekrempelt.

Kein Google Docs mehr. Kein Notion. Kein verzweifeltes Suchen nach "diesem einen Draft von vor drei Wochen".

Stattdessen: **Obsidian**. Eine unscheinbare Notiz-App, die sich als perfekte Blogger-Zentrale entpuppt hat.

Das Beste? Deine Texte gehören DIR. Keine Cloud. Keine Abhängigkeit. Nur Markdown-Files auf deiner Festplatte.

Hier ist, warum das für dich als Blogger Gold wert ist.

## Was bekommst du hier?

In den nächsten 5 Minuten zeige ich dir:
- **Warum** Obsidian deine Content-Organisation verändert
- **Wie** du damit effizienter bloggst (konkrete Beispiele)
- **Was** es kostet (Spoiler: 0€ für die wichtigsten Features)
- **Welche Alternativen** es gibt (ehrlicher Vergleich)

Mit Screenshots, echten Use-Cases aus meiner Blog-Praxis und ohne Werbung.

## Was ist Obsidian überhaupt?

**Elevator Pitch**: Obsidian ist eine Notiz-App, die deine Texte als simple Markdown-Dateien speichert und sie intelligent vernetzt – wie ein persönliches Wikipedia nur für deine Ideen.

**Für wen?**
- Blogger, die **viele Themen** gleichzeitig jonglieren
- Leute, die **keine Cloud** für ihre Drafts wollen
- Alle, die **Zusammenhänge** zwischen Posts sehen wollen
- Menschen, die **Kontrolle über ihre Daten** schätzen

**Nicht für:**
- Reine "Schreiben & Vergessen"-Blogger
- Wer nur 1-2 Posts pro Monat schreibt
- Teams, die Echtzeit-Kollaboration brauchen (dafür gibt's bessere Tools)

## Warum ich von Notion zu Obsidian gewechselt bin

**Mein alter Workflow** (Notion):
1. Idee notieren
2. Irgendwann Draft schreiben
3. Draft verlieren in 47 Unterpages
4. Neu schreiben
5. Repeat

**Problem**: Alles war isoliert. Jeder Post ein Silo. Connections zwischen Themen? Fehlanzeige.

**Mein Obsidian-Workflow jetzt**:
1. Idee notieren mit `[[Tag zur Kategorie]]`
2. Draft schreiben, dabei automatisch mit verwandten Posts verlinken
3. Graph-View anschauen: "Ach, zu dem Thema habe ich ja schon 3 Posts!"
4. Interne Links einfügen
5. Leser bleiben länger (weil zusammenhängende Inhalte)

**Der Unterschied**: Obsidian zeigt mir mein Blog als **Wissensnetzwerk**, nicht als Datei-Friedhof.

## Konkrete Use-Cases für Blogger

### 1. Post-Ideen sammeln (ohne sie zu verlieren)

**Problem**: Du hast ständig Ideen, aber keine Struktur.

**Lösung in Obsidian**:
```markdown
# Post-Ideen

- [[Warum Ghost besser als WordPress ist]] #tutorial
- [[MCP Server einfach erklärt]] #für-einsteiger
- [[Self-Hosting kostet 3€ im Monat]] #digitale-souveränität
```

Klicke auf `[[Titel]]` → neue Datei wird erstellt. Sofort loslegen!

**Warum das funktioniert**: Wikilinks (die `[[ ]]`-Syntax) erstellen automatisch Verbindungen. Später siehst du, welche Ideen zusammengehören.

### 2. Content-Recycling leicht gemacht

**Szenario**: Du schreibst über Docker. Hast du nicht vor 2 Monaten schon was über Container geschrieben?

**In Google Docs**: Wühlen. Suchen. Aufgeben. Neu schreiben.

**In Obsidian**: Tippe `[[` → alle Posts mit "Docker" oder "Container" werden vorgeschlagen. Klick → sofort drin.

**Zeit gespart**: 15 Minuten pro Post (bei mir).

### 3. Themen-Cluster erkennen

Obsidian hat eine **Graph View** – eine visuelle Karte deiner Posts.

**Was du siehst**:
- Welche Themen du oft behandelst (dicke Knoten)
- Welche Posts isoliert sind (einsame Punkte)
- Wo Verbindungen fehlen

**Mein Aha-Moment**: Ich hatte 8 Posts über KI-Tools, aber keinen einzigen Post, der sie vergleicht. Lücke erkannt → neuer Post geschrieben → mehr Traffic.

### 4. Direkt zu Ghost publishen

Mit dem **"Send to Ghost" Plugin** (kostenlos):
1. Post fertig schreiben
2. `Strg+P` → "Send to Ghost"
3. Wähle: Draft oder direkt veröffentlichen
4. Fertig!

**Bonus**: Frontmatter (die YAML-Metadaten oben) werden automatisch übernommen. Tags, Excerpt, alles.

## Setup: So startest du (15 Minuten)

### Was du brauchst
- **Obsidian** (kostenlos) → [obsidian.md](https://obsidian.md)
- **15 Minuten** Zeit
- **Optional**: Ghost-Blog (für das Publishing-Plugin)

### Schritt 1: Vault erstellen

1. Obsidian herunterladen & öffnen
2. "Create new vault" klicken
3. Name: z.B. "Blog Content"
4. Ort: Wo auch immer deine Dateien liegen sollen (z.B. `Dokumente/Blog`)

✅ **Checkpoint**: Du siehst jetzt eine leere Obsidian-Oberfläche.

### Schritt 2: Ordner-Struktur anlegen

Erstelle diese Ordner (Rechtsklick im Datei-Explorer):
```
📁 Blog Content/
  📁 Posts/
  📁 Drafts/
  📁 Ideas/
  📁 Templates/
```

**Warum?**
- `Posts/`: Fertige Artikel
- `Drafts/`: Work in Progress
- `Ideas/`: Schnelle Notizen
- `Templates/`: Wiederkehrende Strukturen

### Schritt 3: Template erstellen

1. Neue Datei in `Templates/` → "Blog Post.md"
2. Füge das ein:

```markdown
---
title: "{{title}}"
tags:
  -
excerpt: ""
status: draft
featured: false
---

# {{title}}

## Hook
[Warum sollte jemand das lesen?]

## Versprechen
Was lernt der Leser?

## Hauptteil
[Content hier]

## Fazit
[Zusammenfassung + CTA]
```

3. Speichern!

**Nutzen**: Neuer Post? Einfach Template kopieren, umbenennen, loslegen.

### Schritt 4: Erste Posts migrieren

Falls du schon Posts in Google Docs/Notion hast:
1. Copy & Paste in neue `.md` Datei
2. Frontmatter hinzufügen (siehe Template)
3. Speichern unter `Posts/2025-12-19-mein-post.md`

**⚠️ Fallstrick**: Dateinamen ohne Leerzeichen! Nutze `-` stattdessen.

### Schritt 5: Ghost-Plugin (optional)

Nur wenn du einen [[Ghost Blog Setup|Ghost-Blog]] hast:

1. `Strg+P` → "Community Plugins" durchsuchen
2. Suche "Ghost"
3. Installiere "Send to Ghost"
4. In Settings: Ghost-URL + API-Key eintragen
5. Fertig!

**API-Key holen**: Ghost Admin → Settings → Integrations → "Add custom integration"

✅ **Checkpoint**: Du kannst jetzt `Strg+P` → "Send to Ghost" nutzen.

## Kosten im Überblick

| Feature | Kosten | Wofür? |
|---------|--------|--------|
| **Obsidian (lokal)** | 0€ | Alle Basis-Features, unbegrenzt |
| **Sync (Cloud-Backup)** | 10$/Monat | Geräte-Sync (optional!) |
| **Publish** | 20$/Monat | Öffentliches Wiki (brauchst du nicht) |
| **Community Plugins** | 0€ | Send to Ghost, etc. |

**Wichtig**: Die kostenpflichtigen Features brauchst du **nicht**!
- Sync? → Nutze Dropbox, Google Drive, oder Git (kostenlos)
- Publish? → Du hast ja Ghost/deine eigene Plattform

**Meine Kosten**: 0€ (nutze Git für Backups)

## Obsidian vs. Alternativen

### Notion
✅ **Besser für**: Teams, Datenbanken, Kollaboration
❌ **Schlechter bei**: Performance, Offline-Arbeit, Datenhoheit

**Fazit**: Super für Teams, aber für Solo-Blogger ist Obsidian schneller & flexibler.

### Logseq
✅ **Besser für**: Outliner-Fans, Aufgaben-Management
❌ **Schlechter bei**: Long-Form-Writing, Übersichtlichkeit

**Fazit**: Wenn du in Bullet-Points denkst: Logseq. Für Blog-Posts: Obsidian.

### Google Docs
✅ **Besser für**: Kommentare, Vorschläge, Teilen
❌ **Schlechter bei**: Organisation, Verlinkungen, Offline

**Fazit**: Für einzelne Kollaborations-Docs okay. Für dein Content-System? Zu chaotisch.

### Evernote / Apple Notes
✅ **Besser für**: Schnelle Notizen, Mobile
❌ **Schlechter bei**: Struktur, Verlinkungen, Export

**Fazit**: Für Einkaufslisten super. Für ernsthafte Blogger? Zu limitiert.

## Was mich überrascht hat

### Positiv ⭐
1. **Graph View ist kein Gimmick**: Ich entdecke wirklich Content-Lücken
2. **Markdown = Freiheit**: Meine Texte funktionieren überall (Ghost, GitHub, etc.)
3. **Offline-First**: Kein Internet? Kein Problem. Schreib einfach weiter.
4. **Community Plugins**: Es gibt ALLES (Kalender, Kanban, Publishing...)

### Negativ ⚠️
1. **Lernkurve**: Die ersten 2 Tage war ich verwirrt (so viele Plugins!)
2. **Kein Echtzeit-Collaboration**: Für Solo-Blogger egal, für Teams ein Deal-Breaker
3. **Mobile App ist... okay**: Funktioniert, aber Desktop ist besser

## Lohnt sich das für dich?

### ✅ Ja, wenn du:
- Mehr als **5 Posts pro Monat** schreibst
- **Themen vernetzt** behandelst (z.B. Tutorial-Serien)
- **Kontrolle über deine Daten** willst (kein Cloud-Zwang)
- Gerne in **Markdown** schreibst (oder es lernen willst)
- Einen [[Ghost Blog Setup|eigenen Blog]] hast (wegen Publishing-Plugin)

### ❌ Nein, wenn du:
- Nur **gelegentlich** bloggst (1-2x/Monat)
- **Team-Collaboration** in Echtzeit brauchst
- Dich mit **Plain-Text-Dateien unwohl** fühlst
- Eine **All-in-One-Lösung** bevorzugst (dann: Notion)

### Mein Fazit

Für mich war der Wechsel zu Obsidian die beste Entscheidung seit... ich blogge.

**Warum?**
- Meine Posts sind jetzt ein **Netzwerk**, kein Haufen isolierter Texte
- Ich finde alte Ideen wieder (Graph View sei Dank)
- Meine Daten gehören **mir** (Markdown-Files auf meiner Festplatte)
- Der Workflow von Idee → Draft → Ghost ist **nahtlos**

**Zeit gespart**: ~2 Stunden pro Woche (durch bessere Organisation & wiederverwendbare Inhalte)

**Einziger Nachteil**: Ich hätte früher wechseln sollen.

## Probier's selbst aus

**Quick-Start (10 Minuten)**:
1. [Obsidian herunterladen](https://obsidian.md)
2. Vault erstellen ("Blog Content")
3. Einen alten Blog-Post reinkopieren
4. Mit `[[` einen zweiten Post verlinken
5. Graph View anschauen (`Strg+G`)

**Was du sehen wirst**: Deine Posts, visuell verbunden. Willkommen in der Matrix deines Contents.

**Fallstrick-Warnung**:
⚠️ Installiere am Anfang **nicht zu viele Plugins**! Die Basis-Features reichen erstmal.
⚠️ Dateinamen: Keine Leerzeichen, nutze `-` (z.B. `mein-post.md`)

## Deine Erfahrungen?

Nutzt du schon Obsidian? Oder schwörst du auf Notion/Google Docs?

Was ist deine größte Herausforderung bei Content-Organisation?

Schreib mir: tristan@digitalalchemisten.de
Oder kommentier direkt hier! 👇

---

**Nächster Post**: Wie du mit [[MCP]] Server deinen Blog automatisierst
**Related**: [[Ghost Blog Setup]] | [[Claude Code für Anfänger]]


---

## Tags erklärt

### Innovation & Tools
**Neue Tools und innovative Ansätze** für digitale Workflows. Hier teste und bewerte ich praktische Tools – immer ehrlich, unabhängig, ohne gesponserte Empfehlungen.

**Fokus:** Was funktioniert wirklich? Was sind die Kosten (auch versteckte)? Welche Alternativen gibt es? Für wen lohnt sich das Tool?

### Für Einsteiger
Posts in dieser Kategorie sind **speziell für Nicht-Techniker** geschrieben. Ich erkläre jeden Schritt, nutze Screenshots bei wichtigen Stellen, weise auf häufige Fehler hin und verzichte auf Fachjargon (oder erkläre ihn sofort).

**Zielgruppe:** CEOs, Quereinsteiger, Wissbegierige – alle, die mitschmischen wollen, aber keine Programmierkenntnisse haben.

### Ghost
**Ghost** ist eine Open-Source Blogging-Plattform. Modern, schnell, fokussiert auf Publishing (statt "alles können" wie WordPress). Mit eingebautem Newsletter-System und REST API für Automatisierung.

**Warum Ghost?** Volle Kontrolle, kein Vendor-Lock-in, perfekt für Self-Hosting, starke Community, regelmäßige Updates.
