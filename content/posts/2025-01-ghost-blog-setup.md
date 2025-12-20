---
title: "Ghost Blog selbst hosten: Von Null auf Live in einer Stunde"
tags:
  - Self-Hosting Tutorials
  - Für Einsteiger
  - Ghost
  - Digitale Souveränität
excerpt: "Du schreibst über digitale Souveränität auf einem US-Server? Ironisch. Hier zeige ich dir, wie du deinen Ghost-Blog in 60 Minuten selbst hostest – für 3€/Monat."
status: draft
featured: true
---

# Ghost Blog selbst hosten: Von Null auf Live in einer Stunde

## Warum überhaupt selbst hosten?

Stell dir vor: Du schreibst einen Blog-Post über digitale Souveränität, aber dein Blog läuft auf einem US-Server, wo Big Tech jeden Klick trackt. Irgendwie ironisch, oder?

Genau deshalb habe ich mich entschieden, meinen Tech-Blog selbst zu hosten. Und das Beste: Es ist viel einfacher als gedacht!

## Was du brauchst

- **Zeit**: 1 Stunde
- **Kosten**: ~3€/Monat (VPS + Domain)
- **Vorkenntnisse**: Keine! Wir machen das zusammen

## Der Plan: Lokal erst, dann live

Hier ist der smarte Ansatz, den ich gewählt habe:

1. **Lokal entwickeln** - Ghost auf deinem Rechner installieren
2. **Content erstellen** - Blog-Posts in Ruhe schreiben & testen
3. **Dann erst deployen** - Wenn alles steht, ab auf den Server

**Warum?** Spart Zeit, Geld und Nerven. Kein rumfummeln auf einem Live-Server!

## Schritt 1: Ghost lokal mit Docker (5 Minuten)

Docker ist wie ein Mini-Computer in deinem Computer. Klingt kompliziert? Ist es nicht!

```bash
# Ghost Container starten
docker run -d \
  --name ghost-local \
  -p 2368:2368 \
  -e NODE_ENV=development \
  -v ghost-content:/var/lib/ghost/content \
  ghost:latest
```

**Was passiert hier?**
- `docker run` = "Starte einen Container"
- `-p 2368:2368` = "Öffne Port 2368 für den Browser"
- `-v ghost-content` = "Speichere alles dauerhaft"

🎉 **Das war's!** Öffne http://localhost:2368 - dein Blog läuft!

## Schritt 2: Admin-Account erstellen (2 Minuten)

Gehe zu http://localhost:2368/ghost und erstelle deinen Account:

- **Blog-Titel**: Z.B. "Tech für Alle"
- **Name**: Dein Name
- **Email & Passwort**: Wähle was sicheres!

![Ghost Setup Screenshot Platzhalter]

## Schritt 3: Ersten Post schreiben (10 Minuten)

Hier kommt der Clou: **Schreib Posts als Markdown-Files!**

Warum?
- ✅ Versionskontrolle mit Git
- ✅ Backup automatisch
- ✅ Keine Angst vor Datenverlust
- ✅ Schneller als im Editor

Erstelle eine Datei `mein-erster-post.md`:

```markdown
# Mein erster selbstgehosteter Post

Heute habe ich meinen eigenen Blog aufgesetzt.
Keine Abhängigkeit von Medium, Substack oder WordPress.com.

**Das fühlt sich gut an!**

## Was ich gelernt habe

1. Docker ist nicht scary
2. Ghost ist super einfach
3. Selbst hosten macht Spaß
```

Dann in Ghost importieren: Admin → Labs → Import Content

## Schritt 4: GitHub Backup (5 Minuten)

Damit du nie wieder Posts verlierst:

```bash
git init
git add .
git commit -m "Initial commit - Ghost blog setup"
git push origin main
```

Jetzt ist alles gesichert. Laptop kaputt? Kein Problem!

## Was kommt als Nächstes?

**Nächste Woche** zeige ich dir:
- Wie du das auf einen günstigen VPS (2€/Monat) bekommst
- SSL-Zertifikat automatisch einrichten
- CI/CD Pipeline: Git Push → Live Update

**In 2 Wochen**:
- Custom Theme designen
- Newsletter-System einrichten
- Analytics (DSGVO-konform!)

## Häufige Probleme & Lösungen

### "Docker startet nicht"
→ Docker Desktop neu starten, 30 Sekunden warten

### "Port 2368 schon belegt"
→ Anderes Programm nutzt den Port. Nutze `-p 3000:2368` stattdessen

### "Container verschwindet nach Neustart"
→ Fehlte das `-v ghost-content` beim docker run? Dann sind Daten weg 😢

## Kosten-Check: Was kostet das wirklich?

| Was | Kosten/Monat | Notiz |
|-----|--------------|-------|
| Lokal (Docker) | 0€ | Nur zum Testen |
| VPS (IONOS) | 2€ | Für Live-Blog |
| Domain | 1€ | z.B. .de Domain |
| Email-Versand | 0€ | Mailgun gratis bis 5k/Monat |
| **Total** | **3€** | Günstiger als Netflix! |

## Fazit: Lohnt sich das?

**JA!** Aus diesen Gründen:

1. **Volle Kontrolle**: Deine Daten, dein Server, deine Regeln
2. **Lernerfahrung**: Du verstehst, wie das Web funktioniert
3. **Kosten**: 3€/Monat vs. 15€ für Medium Premium
4. **Flexibilität**: Alles anpassbar, keine Limits

**Aber**: Wenn du nur schnell einen Blog brauchst, nimm Ghost(Pro) oder Medium. Selbst hosten ist für die, die verstehen wollen, wie's läuft!

## Deine Erfahrungen?

Hast du Ghost schon ausprobiert? Was waren deine größten Hürden?

Schreib mir: [deine@email.de]

---

**Related Posts:**
- [[Ghost Blog mit Claude verbinden]] – Claude + Ghost Integration
- [[MCP Server erklärt]] – Wie Claude mit Tools spricht
- [[KI-Assistenten selbst hosten]] – Wann lohnt sich Self-Hosting?

---

## Tags erklärt

### Self-Hosting Tutorials
**Selbst hosten** bedeutet: Deine Dienste (hier: Ghost Blog) laufen auf deinem eigenen Server statt bei Big Tech. In diesem Tutorial zeige ich dir Schritt für Schritt, wie du das machst – auch ohne Vorkenntnisse.

**Warum Self-Hosting?** Kontrolle über deine Daten, keine Abhängigkeit von Plattformen, volle Anpassbarkeit.

### Für Einsteiger
Diese Posts sind **speziell für Nicht-Techniker** geschrieben. Ich erkläre jeden Schritt, nutze Screenshots bei wichtigen Stellen und weise auf häufige Fehler hin. Kein Vorwissen nötig!

### Ghost
**Ghost** ist eine Open-Source Blogging-Plattform. Modern, schnell, fokussiert auf Publishing (statt "alles können" wie WordPress). Perfekt für Blogger, die Kontrolle über ihren Content wollen.

### Digitale Souveränität
**Digitale Souveränität** bedeutet: Du kontrollierst deine digitalen Assets selbst. Keine US-Cloud, keine Abhängigkeit von Plattform-Algorithmen, keine Vendor-Lock-ins. EU-Server, eigene Infrastruktur, eigene Regeln.

---

*Dieser Blog läuft selbst auf Ghost, gehostet auf einem IONOS VPS in Deutschland. 100% EU, 0% Big Tech Tracking.* 🇪🇺
