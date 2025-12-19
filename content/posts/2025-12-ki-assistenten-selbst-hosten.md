# KI-Assistenten selbst hosten: Wann lohnt es sich wirklich?

Letzte Woche fragte mich ein Firmenchef: "Können wir ChatGPT auf unserem eigenen Server laufen lassen?"

Die kurze Antwort: ChatGPT selbst nicht. Aber es gibt Alternativen.

Die längere Antwort: Es kommt darauf an, was du wirklich brauchst – und ich zeige dir in den nächsten 10 Minuten, wie du das herausfindest.

## Was du in diesem Post lernst

In den nächsten 10 Minuten zeige ich dir:
- **Was** "selbst hosten" wirklich bedeutet (ohne Technik-Sprech)
- **Wann** es Sinn macht (und wann nicht)
- **Wie viel** es kostet (transparent, alle Kosten)
- **Welche Alternativen** es gibt (unabhängig bewertet)

Mit echten Zahlen, ehrlichen Einschätzungen und ohne Tool-Werbung.

## Was bedeutet "selbst hosten" überhaupt?

**Stell dir vor**, du nutzt ChatGPT im Browser:
- Deine Daten gehen zu OpenAI (USA)
- OpenAI verarbeitet alles
- Du zahlst pro Nutzung
- OpenAI kann jederzeit Preise ändern oder Features entfernen

**Beim Self-Hosting**:
- Die KI läuft auf **deinem** Server (oder einem gemieteten in der EU)
- Deine Daten bleiben bei dir
- Du kontrollierst alles
- Aber: Du kümmerst dich auch um alles

**Das ist wie**: Taxi vs. eigenes Auto
- Taxi (Cloud): Einfach, aber teuer & abhängig
- Eigenes Auto (Self-Hosting): Kontrolle, aber Verantwortung

## Für wen lohnt sich Self-Hosting?

### ✅ Ja, wenn:

**1. Sensible Daten**
- Du verarbeitest Kundendaten, Gesundheitsdaten, Finanzdaten
- DSGVO-Compliance ist kritisch
- Deine Branche verbietet Cloud-Dienste außerhalb der EU

**Beispiel**: Rechtsanwaltskanzlei, die Mandantendaten mit KI analysieren will.

**2. Langfristige Kosten-Kontrolle**
- Du nutzt KI täglich, viele Anfragen
- Cloud-Kosten sind unvorhersehbar
- Du willst fixe Kosten statt "pay per use"

**Beispiel**: Marketing-Agentur, die täglich 1000+ Social-Media-Posts analysiert.

**3. Digitale Souveränität**
- Du willst unabhängig von US-Anbietern sein
- Du willst die KI anpassen können
- Dir ist Kontrolle wichtiger als Bequemlichkeit

**Beispiel**: Bildungseinrichtung, die eine KI für Schüler bereitstellen will.

### ❌ Nein, wenn:

**1. Du testest nur**
- Du willst erstmal ausprobieren
- Du hast noch keinen klaren Use-Case
- Du brauchst schnelle Ergebnisse

**Dann**: Nutze ChatGPT Plus (20$/Monat) oder Claude Pro (20$/Monat) zum Testen.

**2. Kleine Teams, seltene Nutzung**
- Ihr seid 2-5 Leute
- Ihr nutzt KI 1-2x pro Woche
- Einfachheit ist wichtiger als Kosten

**Dann**: Cloud-Dienste sind günstiger & einfacher.

**3. Du brauchst State-of-the-Art**
- Du willst die besten Modelle (GPT-4, Claude Opus)
- Du brauchst die neuesten Features
- Performance ist kritisch

**Dann**: Die besten Modelle gibt's (noch) nur in der Cloud.

## Was kostet Self-Hosting wirklich?

Lass uns ehrlich rechnen. Ich zeige dir ein **realistisches Beispiel** für ein 10-Personen-Team:

### Option 1: Cloud (ChatGPT Team)
**Kosten pro Monat**:
- 10 Nutzer × 25$ = **250$/Monat**
- Keine Setup-Kosten
- Keine Wartung nötig

**Versteckte Kosten**:
- API-Nutzung extra (wenn du eigene Tools baust)
- Preiserhöhungen möglich
- Feature-Changes ohne Mitspracherecht

**Total**: ~250-300$/Monat

### Option 2: Self-Hosted (Llama 3 auf eigenem Server)
**Einmalige Kosten**:
- Server-Setup: 100-200€ (oder du machst es selbst)

**Monatliche Kosten**:
- VPS (Hetzner Cloud CPX51): 50€/Monat
  - 16 vCPU, 32 GB RAM, 360 GB SSD
- Oder dedizierter Server (mehr Power): 80-150€/Monat

**Wartung**:
- Updates: 2-4 Stunden/Monat
- Dein Zeit-Invest oder IT-Dienstleister (150€/h)

**Total**: 50-200€/Monat + Zeitaufwand

### Option 3: Hybrid (Das Beste aus beiden Welten)
**Setup**:
- Cloud für explorative Arbeit (ChatGPT Plus)
- Self-Hosted für Routine-Aufgaben & sensible Daten

**Kosten**:
- 3 Cloud-Accounts (Entscheider): 60$/Monat
- Self-Hosted für Team: 50€/Monat

**Total**: ~110€/Monat

## Konkrete Self-Hosting-Lösungen (ohne Programmieren)

### 1. Jan.ai – Die einfachste Option

**Was ist das?**
Jan ist wie "ChatGPT für deinen Computer". Du lädst es herunter, fertig.

**Für wen?**
Einzelpersonen oder kleine Teams, die offline arbeiten wollen.

**Setup-Zeit**: 15 Minuten
**Kosten**: 0€ (Open Source)
**Daten**: Bleiben auf deinem PC

**Installation**:
1. Gehe zu jan.ai
2. Download für Windows/Mac/Linux
3. Öffne Jan
4. Wähle ein Modell (z.B. Llama 3 8B)
5. Fertig!

**✅ Vorteile**:
- Komplett kostenlos
- Keine Cloud, alles lokal
- Sehr einfach

**❌ Nachteile**:
- Läuft nur auf einem Gerät
- Braucht guten PC (16GB RAM empfohlen)
- Nicht so gut wie ChatGPT/Claude

**Lohnt sich für**: Datenschutz-Bewusste, die testen wollen.

### 2. Ollama + Open WebUI – Für Teams

**Was ist das?**
Ollama ist eine Software, die KI-Modelle auf Servern laufen lässt.
Open WebUI ist die Benutzeroberfläche (sieht aus wie ChatGPT).

**Für wen?**
Teams, die eine gemeinsame KI-Instanz wollen.

**Setup-Zeit**: 2-3 Stunden (mit Anleitung)
**Kosten**: 30-80€/Monat (Server)
**Daten**: Auf deinem Server (EU möglich)

**Was du brauchst**:
- Server bei Hetzner/IONOS/Contabo (ab 30€/Monat)
- 2-3 Stunden zum Setup (folge der Anleitung auf ollama.com)
- Kein Programmier-Wissen, aber "Copy-Paste-Skills"

**✅ Vorteile**:
- Team kann gemeinsam nutzen
- Viele Modelle zur Auswahl
- Volle Kontrolle

**❌ Nachteile**:
- Server-Verwaltung nötig
- Technisches Setup erforderlich
- Updates musst du selbst machen

**Lohnt sich für**: Teams ab 5 Personen mit IT-affiner Person.

### 3. Hugging Face Inference Endpoints – Managed Self-Hosting

**Was ist das?**
Hugging Face hostet die KI für dich, aber auf **deinem** dedizierten Server.

**Für wen?**
Unternehmen, die Kontrolle wollen, aber keine Wartung.

**Setup-Zeit**: 30 Minuten
**Kosten**: 60-500€/Monat (je nach Modell-Größe)
**Daten**: Auf EU-Servern möglich

**✅ Vorteile**:
- Einfaches Setup
- Wartung übernimmt Hugging Face
- DSGVO-konform möglich

**❌ Nachteile**:
- Teurer als DIY
- Immer noch "Vendor" (Hugging Face)
- Technisches Verständnis für API nötig

**Lohnt sich für**: Unternehmen mit Budget, die Kontrolle + Einfachheit wollen.

## Transparenz-Check: Alternativen & ihre Trade-offs

Ich bewerte hier **unabhängig** – keine Affiliate-Links, keine gesponserten Empfehlungen.

| Lösung | Kosten/Monat | Setup | DSGVO | Performance | Für wen? |
|--------|--------------|-------|-------|-------------|----------|
| **ChatGPT Plus** | 20$ | 5 Min | ❌ USA | ⭐⭐⭐⭐⭐ | Einzelnutzer, Testen |
| **Claude Pro** | 20$ | 5 Min | ❌ USA | ⭐⭐⭐⭐⭐ | Einzelnutzer, Testen |
| **Jan.ai (lokal)** | 0€ | 15 Min | ✅ Lokal | ⭐⭐⭐ | Privacy-First, Offline |
| **Ollama + Open WebUI** | 30-80€ | 2-3 Std | ✅ EU | ⭐⭐⭐⭐ | Teams, DIY |
| **HuggingFace Endpoints** | 60-500€ | 30 Min | ✅ EU | ⭐⭐⭐⭐ | Unternehmen |
| **ChatGPT Team** | 250$ (10 User) | 10 Min | ❌ USA | ⭐⭐⭐⭐⭐ | Teams, einfach |

## Meine ehrliche Empfehlung (nach 6 Monaten Testing)

Nach 6 Monaten, in denen ich alle Optionen getestet habe, ist mein Setup:

**Für mich persönlich**:
- **Claude Pro** für Brainstorming & komplexe Aufgaben
- **Ollama** (lokal) für sensible Daten & Experimente

**Warum?**
- Claude ist einfach besser für kreative Arbeit
- Ollama nutze ich für Kundendaten, die nicht in die Cloud sollen
- Hybrid-Ansatz: Das Beste aus beiden Welten

**Was ich NICHT empfehle** (für die meisten):
- Komplett auf Cloud verzichten → du verlierst zu viel Performance
- Komplett auf Self-Hosting setzen → zu viel Aufwand für wenig Nutzen
- Alles selbst programmieren → es gibt gute Tools, nutze sie!

## Deine nächsten Schritte

### Wenn du nur testen willst:
1. Hol dir ChatGPT Plus oder Claude Pro (je 20$/Monat)
2. Teste 1 Monat intensiv
3. Entscheide dann, ob du mehr Kontrolle brauchst

### Wenn du selbst hosten willst:
1. **Start simple**: Installiere Jan.ai auf deinem PC (kostenlos, 15 Min)
2. **Teste Anwendungsfälle**: Funktioniert das Modell für deine Aufgaben?
3. **Skaliere wenn nötig**: Wenn Jan gut läuft, miete einen Server für Ollama

### Wenn du Unterstützung brauchst:
- **Ollama Setup-Guide**: ollama.com/download (sehr gute Anleitung)
- **Open WebUI Docs**: docs.openwebui.com
- **Hetzner Cloud Tutorial**: Suche "Ollama Hetzner Setup" auf YouTube

## Lohnt sich Self-Hosting für dich?

**Ja, wenn:**
- Du sensible Daten verarbeitest (DSGVO-kritisch)
- Du langfristig Kosten sparen willst (viele Anfragen/Tag)
- Dir digitale Souveränität wichtig ist
- Du Zeit für Setup/Wartung hast (oder jemanden im Team)

**Nein, wenn:**
- Du nur testest oder selten nutzt
- Du die besten Modelle willst (GPT-4, Claude Opus)
- Einfachheit wichtiger als Kontrolle ist
- Du kein Budget für Server-Miete hast

**Für mich** war der Hybrid-Ansatz der richtige Weg: Cloud für Performance, Self-Hosting für Kontrolle.

Was passt zu dir?

## Deine Erfahrungen?

Nutzt du schon KI-Tools? Cloud oder selbst gehostet?
Was war deine größte Hürde?

Schreib mir: tristan@digitalalchemisten.de
Oder kommentier direkt hier! 👇

---

**Nächster Post**: Wie ich meinen Ghost-Blog mit Claude verbinde (ohne Programmieren)
**Related**: [Digitale Souveränität vs. Convenience: Der ewige Trade-off]

**Disclaimer**: Ich bekomme kein Geld von den genannten Tools. Alle Empfehlungen basieren auf eigener Erfahrung nach 6 Monaten Testing.
