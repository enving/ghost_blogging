# MCP Server erklärt: Wie Claude mit deinen Tools spricht

**Schwierigkeitsgrad**: Fortgeschritten
**Zeit**: 15 Minuten Lesezeit
**Konzepte**: APIs, Automation, KI-Integration

## Das Problem mit KI-Assistenten

Du kennst das vielleicht: Claude ist mega hilfreich für Code, Texte und Ideen. Aber er lebt in seiner eigenen Bubble. Er kann nicht:

- Auf deine Datenbank zugreifen
- Blog-Posts für dich publishen
- Mit deinen Tools sprechen
- Automatisch Workflows ausführen

**Lösung**: MCP Server (Model Context Protocol)

## Was ist ein MCP Server?

Stell dir vor, Claude ist ein super intelligenter Praktikant. Er kann alles - aber er hat keinen Zugang zu deinen Systemen.

**MCP Server = Die Zugangskarte**

Ein MCP Server ist eine Brücke zwischen Claude und deiner Software:

```
Claude  ←→  MCP Server  ←→  Deine Tools
         (Die Brücke)        (Ghost, DB, APIs)
```

## Beispiel: Ghost MCP Server

Ich nutze einen MCP Server für meinen Ghost-Blog. Was er kann:

### Ohne MCP:
1. Ich sage Claude: "Schreib einen Post über Docker"
2. Claude schreibt den Text
3. Ich kopiere ihn in Ghost
4. Ich klicke auf "Publish"
5. Ich checke, ob alles okay ist

**Problem**: Viele manuelle Schritte!

### Mit MCP:
1. Ich sage Claude: "Schreib und veröffentliche einen Post über Docker"
2. **Fertig!**

Claude nutzt den MCP Server um:
- Den Post zu erstellen
- Formatierung einzufügen
- Tags hinzuzufügen
- Zu publishen
- Newsletter zu verschicken

## Wie funktioniert das technisch?

Der Ghost MCP Server ist ein Node.js-Programm, das:

1. **Auf Claude hört**: Wartet auf Befehle
2. **Ghost Admin API nutzt**: Hat Zugriff auf deinen Blog
3. **Aktionen ausführt**: Erstellt, updated, löscht Posts
4. **Feedback gibt**: "Post erstellt, hier der Link!"

### Setup in 3 Schritten:

```bash
# 1. MCP Server installieren
git clone https://github.com/MFYDev/ghost-mcp
npm install && npm run build

# 2. Konfigurieren
GHOST_API_URL=http://localhost:2368
GHOST_ADMIN_API_KEY=dein-key-hier

# 3. In Claude einbinden
# → Claude Desktop Settings → MCP Servers
```

## Wann solltest du MCP nutzen?

### ✅ Perfekt für:

- **Bulk-Operations**: 100 Posts auf einmal taggen
- **Automation**: Newsletter jeden Sonntag automatisch
- **Member-Management**: Nutzer-Verwaltung
- **Analytics**: Reports automatisch generieren

### ❌ Nicht ideal für:

- **Normale Posts schreiben**: Markdown ist schneller
- **Einmalige Aktionen**: Direkter Zugriff ist einfacher
- **Learning**: Versteck die Komplexität nicht zu früh

## Der Token-Trick: Markdown First!

Hier ist mein Workflow, der 80% Tokens spart:

```
Alte Methode (teuer):
Claude + MCP → API Call → Post erstellt
(Viele Tokens pro Request!)

Neue Methode (günstig):
Claude → Markdown File → Du importierst
(Normale Read/Write Tools, kaum Tokens!)
```

**MCP nur für**:
- Newsletter-Versand
- Bulk-Updates
- Scheduled Publishing

## Beispiel-Use-Cases

### Use Case 1: Wöchentlicher Newsletter

```javascript
// Jeden Sonntag um 10:00
"Claude, sende Newsletter mit allen Posts dieser Woche"

→ MCP Server holt Posts
→ Generiert Newsletter-Text
→ Versendet an alle Subscriber
```

### Use Case 2: Content-Migration

```javascript
"Claude, importiere alle meine Medium-Posts nach Ghost"

→ MCP Server liest Medium Export
→ Konvertiert zu Ghost-Format
→ Erstellt alle Posts
→ Setzt korrekte Dates
```

### Use Case 3: SEO-Optimierung

```javascript
"Claude, update alle Posts ohne Meta-Description"

→ MCP findet Posts ohne Meta
→ Generiert passende Descriptions
→ Updated alle auf einmal
```

## Andere coole MCP Server

Ghost ist nur der Anfang. Es gibt MCP Server für:

- **GitHub**: Automatische PRs, Issue-Management
- **Notion**: Datenbank-Updates, Content-Sync
- **Slack**: Message-Automation
- **Airtable**: Daten-Management
- **Puppeteer**: Browser-Automation

## Sicherheit: Das musst du wissen

⚠️ **Wichtig**: MCP Server haben VOLLEN Zugriff auf deine Systeme!

### Best Practices:

1. **Nie API-Keys in Code**: Nutze Environment Variables
2. **Read-Only wo möglich**: Nicht jeder MCP braucht Write-Access
3. **Lokal erst testen**: Bevor du Production-Keys nutzt
4. **Logs checken**: Was macht der MCP wirklich?

### Mein Setup:

```bash
# Lokal: Test-Umgebung
GHOST_API_URL=http://localhost:2368
GHOST_ADMIN_API_KEY=test-key

# Production: Nur wenn nötig
# Und: MCP Server "disabled" in Config
# Aktiviere nur für spezielle Tasks
```

## Die Zukunft: Agentic Workflows

MCP Server sind der Anfang von etwas Größerem:

**Heute**:
"Claude, schreib einen Post" → Du checkst & publishst

**Morgen**:
"Claude, manage meinen Blog" → Er macht alles:
- Content-Kalender
- SEO-Optimierung
- Newsletter-Timing
- Analytics-Reports
- Community-Management

**= Agentic AI**

## Probier's aus!

### Quick Start:

1. **Ghost lokal starten** (siehe meinen anderen Post)
2. **Ghost MCP installieren**: https://github.com/MFYDev/ghost-mcp
3. **Test-Post erstellen** via Claude
4. **Mind = Blown** 🤯

### Tutorial-Serie:

- **Teil 1**: MCP Server Setup (dieser Post)
- **Teil 2**: Custom MCP Server bauen (nächste Woche)
- **Teil 3**: Multi-MCP Workflows (in 2 Wochen)

## Deine Fragen

**Q: Kostet MCP Server extra?**
A: Nein! Aber: Claude-API-Calls kosten Tokens.

**Q: Kann ich eigene MCP Server bauen?**
A: Ja! Mit Node.js, Python oder Go.

**Q: Ist das sicher?**
A: Ja, wenn du API-Keys schützt und Logs checkst.

**Q: Brauche ich das wirklich?**
A: Nur wenn du viel automatisieren willst. Für normale Blogs: Nein.

## Fazit

MCP Server sind wie Superkräfte für Claude:

- ✅ Automatisierung von wiederkehrenden Tasks
- ✅ Integration mit deinen Tools
- ✅ Zeitersparnis bei Bulk-Operations

**Aber**: Nicht für alles sinnvoll. Markdown-First ist oft besser!

Meine Regel:
- **80% der Zeit**: Markdown Files
- **20% der Zeit**: MCP für Automation

Was würdest du automatisieren?

---

**Tags**: #MCP #Claude #Automation #Ghost #AI-Integration
**Serie**: KI-Automation (Teil 1/3)
**Related**: Ghost Blog Setup, Docker für Anfänger

---

*Fun Fact: Dieser Post wurde zu 100% von Claude geschrieben. Aber ich habe ihn als Markdown gespeichert, nicht via MCP. 😉*
