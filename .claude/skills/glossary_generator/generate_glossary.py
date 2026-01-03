#!/usr/bin/env python3
"""
Extrahiert technische Begriffe aus Blog-Posts und erstellt automatisch Glossar-Einträge.
"""

import re
from pathlib import Path
from collections import Counter

# Technische Begriffe die wir im Glossar erklären wollen
TECH_TERMS = {
    'MCP': 'Model Context Protocol',
    'Ghost': 'Ghost CMS',
    'VPS': 'Virtual Private Server',
    'API': 'Application Programming Interface',
    'DSGVO': 'Datenschutz-Grundverordnung',
    'Claude': 'Claude AI Assistant',
    'Docker': 'Container-Technologie',
    'SSH': 'Secure Shell',
    'SSL': 'Secure Sockets Layer',
    'SEO': 'Search Engine Optimization',
    'JWT': 'JSON Web Token',
    'OAuth': 'Open Authorization',
    'CI/CD': 'Continuous Integration/Continuous Deployment',
    'Node.js': 'JavaScript Runtime',
    'Python': 'Programmiersprache',
    'Markdown': 'Markup-Sprache',
    'YAML': 'YAML Ain\'t Markup Language',
    'JSON': 'JavaScript Object Notation',
    'Git': 'Versionskontrollsystem',
    'GitHub': 'Code-Hosting-Plattform',
    'Nginx': 'Webserver',
    'MySQL': 'Datenbank',
    'Self-Hosting': 'Selbst-Hosting',
    'Open Source': 'Quelloffene Software',
    'KI': 'Künstliche Intelligenz',
    'AI': 'Artificial Intelligence',
    'LLM': 'Large Language Model',
    'Obsidian': 'Note-Taking App',
    'Wikilinks': 'Wiki-Verlinkungen',
    'Frontmatter': 'Metadaten-Header',
}

GLOSSAR_DEFINITIONS = {
    'MCP': """**MCP (Model Context Protocol)** ist eine Brücke zwischen KI-Assistenten wie Claude und deinen Tools.

**Praktisch bedeutet das:** Statt nur zu chatten, kann Claude durch MCP direkt mit deinem Ghost-Blog, deiner Datenbank oder anderen Tools interagieren – als wäre es ein Teammitglied mit Zugriff auf deine Systeme.

**Beispiel:** Mit MCP kann Claude direkt Blog-Posts in Ghost erstellen, Newsletter verschicken oder Datenbank-Abfragen durchführen.""",

    'Ghost': """**Ghost** ist eine moderne Open-Source Blogging-Plattform.

**Warum Ghost?**
- Fokussiert auf Publishing (nicht "alles können" wie WordPress)
- Eingebautes Newsletter-System
- REST API für Automatisierung
- Schnell & modern
- Perfekt für Self-Hosting

**Alternative zu:** WordPress, Medium, Substack""",

    'VPS': """**VPS (Virtual Private Server)** ist dein eigener Miniserver in einem Rechenzentrum.

**Metapher:** Wie eine Wohnung in einem Mehrfamilienhaus – dein eigener Raum, aber das Gebäude teilst du.

**Praktisch:** Du mietest Server-Ressourcen (CPU, RAM, Speicher) und kannst darauf installieren was du willst.

**Kosten:** Ab 2-5€/Monat (z.B. IONOS, Hetzner)""",

    'API': """**API (Application Programming Interface)** ist eine Schnittstelle zwischen Programmen.

**Einfach erklärt:** Wie eine Speisekarte im Restaurant – du bestellst (API-Request), die Küche macht's (Backend), du bekommst dein Essen (API-Response).

**Beispiel:** Ghost Admin API ermöglicht es Claude, Blog-Posts zu erstellen ohne die UI zu nutzen.""",

    'DSGVO': """**DSGVO (Datenschutz-Grundverordnung)** ist das EU-Datenschutzgesetz.

**Wichtig für Blogger:**
- Nutzer müssen zustimmen (Cookie-Consent)
- Daten auf EU-Servern speichern (oder Rechtfertigung)
- Impressum & Datenschutzerklärung Pflicht
- Recht auf Datenlöschung

**Warum relevant:** Self-Hosting in der EU macht DSGVO-Compliance einfacher.""",

    'Claude': """**Claude** ist ein KI-Assistent von Anthropic.

**Besonderheiten:**
- Sehr gut in längeren Gesprächen
- Kann Code schreiben & analysieren
- Respektiert Nutzergrenzen
- Claude Code CLI für Terminal-Integration

**Alternativen:** ChatGPT (OpenAI), Gemini (Google)""",

    'Docker': """**Docker** ist eine Container-Technologie.

**Einfach erklärt:** Ein "Mini-Computer" in deinem Computer. Die Anwendung läuft isoliert mit allen nötigen Dependencies.

**Vorteil:** "Works on my machine" → "Works everywhere"

**Beispiel:** Ghost als Docker-Container starten statt komplizierte Installation.""",

    'SSH': """**SSH (Secure Shell)** ist verschlüsselter Zugang zu Servern.

**Praktisch:** Du verbindest dich sicher mit deinem VPS über die Kommandozeile.

**Beispiel:** `ssh root@deine-server-ip`

**Warum wichtig:** Für Self-Hosting brauchst du SSH-Zugang zu deinem Server.""",

    'SSL': """**SSL/TLS** verschlüsselt die Verbindung zwischen Browser und Server.

**Erkennbar an:** `https://` statt `http://`

**Warum wichtig:**
- Google rankt HTTPS-Seiten besser
- Nutzer vertrauen der Seite
- Pflicht für Login-Formulare

**Kostenlos:** Let's Encrypt (automatisch mit Ghost)""",

    'SEO': """**SEO (Search Engine Optimization)** bedeutet Suchmaschinen-Optimierung.

**Ziel:** Bessere Rankings bei Google & Co.

**Basics für Blogger:**
- Gute Titel & Meta-Descriptions
- Schnelle Ladezeiten
- Mobile-freundlich
- Interne Verlinkungen
- Qualitativ hochwertiger Content

**Nicht:** Keyword-Stuffing, gekaufte Links""",

    'Self-Hosting': """**Self-Hosting** bedeutet: Deine Dienste laufen auf deinem eigenen Server statt bei Big Tech.

**Vorteile:**
- Volle Kontrolle über Daten
- Keine Plattform-Abhängigkeit
- Oft günstiger langfristig
- Digitale Souveränität

**Nachteile:**
- Du bist für Updates/Sicherheit verantwortlich
- Lernkurve am Anfang
- Kein Support-Hotline

**Typisch:** Ghost auf VPS statt Ghost(Pro) oder Medium""",

    'Obsidian': """**Obsidian** ist eine moderne Note-Taking App.

**Besonderheiten:**
- Markdown-basiert
- Wikilinks für Vernetzung
- Graph View (visuell)
- Daten bleiben lokal (Privacy)
- Kostenlos (Sync optional)

**Perfekt für:** Blogger, die Content organisieren & vernetzen wollen

**Alternative zu:** Notion, Evernote, Logseq""",

    'Markdown': """**Markdown** ist eine einfache Markup-Sprache für formatierten Text.

**Beispiel:**
```
# Überschrift
**fett** und *kursiv*
- Liste
[Link](url)
```

**Warum wichtig:**
- Ghost nutzt Markdown
- Obsidian nutzt Markdown
- Versionskontrolle mit Git einfach
- Plattform-unabhängig

**Vorteil:** Fokus auf Schreiben, nicht auf Formatierung""",

    'Git': """**Git** ist ein Versionskontrollsystem.

**Einfach erklärt:** Wie "Änderungen nachverfolgen" in Word, aber für Code/Text.

**Praktisch:** Du kannst jederzeit zu älteren Versionen zurück.

**Beispiel:** Deine Blog-Posts als Markdown-Files in Git → nie wieder Datenverlust.""",

    'GitHub': """**GitHub** ist eine Plattform zum Hosten von Git-Repositories.

**Nutzen für Blogger:**
- Backup deiner Posts
- Versions-Historie
- Zusammenarbeit möglich
- CI/CD für automatisches Deployment

**Alternative:** GitLab, Bitbucket

**Kostenlos:** Für öffentliche und private Repos""",
}

def find_terms_in_text(text):
    """Findet technische Begriffe im Text."""
    found_terms = set()

    for term in TECH_TERMS.keys():
        # Suche nach Begriffen (case-insensitive, aber behalte Original)
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_terms.add(term)

    return found_terms

def create_glossary_entry(term, output_dir):
    """Erstellt einen Glossar-Eintrag."""
    # Sanitize filename (replace problematic characters)
    safe_filename = term.replace('/', '-').replace('\\', '-').replace(':', '-')
    filepath = output_dir / f"{safe_filename}.md"

    if filepath.exists():
        print(f"   ⏭️  {term}.md existiert bereits")
        return False

    definition = GLOSSAR_DEFINITIONS.get(term, f"**{term}** ({TECH_TERMS.get(term, 'Begriff')})")

    content = f"""# {term}

{definition}

---

**Kategorie:** Glossar
**Verwandt mit:** Technische Begriffe, Self-Hosting, KI & Automation
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"   ✅ {term}.md erstellt")
    return True

def main():
    """Main function."""
    posts_dir = Path('content/posts')
    glossar_dir = Path('content/glossar')

    # Erstelle Glossar-Verzeichnis falls nötig
    glossar_dir.mkdir(exist_ok=True)

    print("🔍 Suche nach technischen Begriffen in Posts...\n")

    all_terms = Counter()

    # Durchsuche alle Posts
    for md_file in posts_dir.glob('*.md'):
        if md_file.name.startswith('.'):
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        terms = find_terms_in_text(content)
        for term in terms:
            all_terms[term] += 1

    print(f"📊 Gefundene Begriffe: {len(all_terms)}\n")
    print("=" * 60)

    created = 0
    skipped = 0

    # Erstelle Glossar-Einträge (sortiert nach Häufigkeit)
    for term, count in all_terms.most_common():
        print(f"\n📖 {term} (kommt {count}x vor)")

        if create_glossary_entry(term, glossar_dir):
            created += 1
        else:
            skipped += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"\n✨ Glossar-Update:")
    print(f"   ✅ Erstellt: {created}")
    print(f"   ⏭️  Bereits vorhanden: {skipped}")
    print(f"   📚 Gesamt: {len(list(glossar_dir.glob('*.md')))}")
    print(f"\n📂 Glossar-Ordner: {glossar_dir.absolute()}")

if __name__ == '__main__':
    main()
