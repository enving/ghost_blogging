#!/usr/bin/env python3
"""
Fügt automatisch Tags-Glossar zu allen Blog-Posts hinzu.
Basierend auf den Tags im Frontmatter.
"""

import os
import re
from pathlib import Path

# Tags-Definitionen
TAG_DEFINITIONS = {
    "KI & Automation": """**Künstliche Intelligenz (KI) und Automatisierung** – Posts in dieser Kategorie zeigen, wie moderne KI-Tools wie Claude, ChatGPT oder selbstgehostete Modelle deine Workflows automatisieren können. Nicht als Ersatz für menschliches Denken, sondern als intelligentes Werkzeug.

**Praktisch bedeutet das:** Von Content-Erstellung über Code-Generation bis hin zu automatisierten Prüfungen – immer mit dem Fokus auf praktischer Anwendung für Non-Techies.""",

    "Self-Hosting Tutorials": """**Selbst hosten** bedeutet: Deine Dienste (Blog, KI, Datenbank) laufen auf deinem eigenen Server statt bei Big Tech-Anbietern. Diese Tutorials zeigen dir Schritt für Schritt, wie du das machst – auch ohne Programmierkenntnisse.

**Warum Self-Hosting?** Kontrolle über deine Daten, keine Abhängigkeit von Plattformen, volle Anpassbarkeit, oft günstiger als Cloud-Dienste.""",

    "Digitale Souveränität": """**Digitale Souveränität** bedeutet: Du kontrollierst deine digitalen Assets selbst. Keine US-Cloud mit unklaren Datenschutzregeln, keine Abhängigkeit von Plattform-Algorithmen, keine Vendor-Lock-ins.

**Konkret:** EU-Server, eigene Infrastruktur, Open-Source-Software, eigene Regeln. Besonders relevant im Kontext von DSGVO und digitaler Selbstbestimmung.""",

    "Innovation & Tools": """**Neue Tools und innovative Ansätze** für digitale Workflows. Hier teste und bewerte ich praktische Tools – immer ehrlich, unabhängig, ohne gesponserte Empfehlungen.

**Fokus:** Was funktioniert wirklich? Was sind die Kosten (auch versteckte)? Welche Alternativen gibt es? Für wen lohnt sich das Tool?""",

    "Privacy & Security": """**Datenschutz und IT-Sicherheit** – verständlich erklärt. Von DSGVO-Compliance über sichere Server-Konfiguration bis hin zu verschlüsselter Kommunikation.

**Praxisnah:** Keine Panikmache, keine theoretischen Diskussionen, sondern konkrete Anleitungen für besseren Datenschutz im Alltag.""",

    "Für Einsteiger": """Posts in dieser Kategorie sind **speziell für Nicht-Techniker** geschrieben. Ich erkläre jeden Schritt, nutze Screenshots bei wichtigen Stellen, weise auf häufige Fehler hin und verzichte auf Fachjargon (oder erkläre ihn sofort).

**Zielgruppe:** CEOs, Quereinsteiger, Wissbegierige – alle, die mitschmischen wollen, aber keine Programmierkenntnisse haben.""",

    "Ghost": """**Ghost** ist eine Open-Source Blogging-Plattform. Modern, schnell, fokussiert auf Publishing (statt "alles können" wie WordPress). Mit eingebautem Newsletter-System und REST API für Automatisierung.

**Warum Ghost?** Volle Kontrolle, kein Vendor-Lock-in, perfekt für Self-Hosting, starke Community, regelmäßige Updates."""
}

def extract_tags_from_frontmatter(content):
    """Extrahiert Tags aus YAML Frontmatter."""
    # Suche nach tags:-Sektion im Frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return []

    frontmatter = frontmatter_match.group(1)

    # Extrahiere tags
    tags = []
    in_tags_section = False
    for line in frontmatter.split('\n'):
        if line.strip().startswith('tags:'):
            in_tags_section = True
            continue
        if in_tags_section:
            if line.strip().startswith('-'):
                tag = line.strip()[1:].strip().strip('"').strip("'")
                tags.append(tag)
            elif not line.startswith(' ') and line.strip():
                break  # Ende der tags-Sektion

    return tags

def generate_tag_glossary(tags):
    """Generiert die Tags-Glossar-Sektion."""
    if not tags:
        return ""

    glossary = "\n---\n\n## Tags erklärt\n\n"

    for tag in tags:
        if tag in TAG_DEFINITIONS:
            glossary += f"### {tag}\n{TAG_DEFINITIONS[tag]}\n\n"

    return glossary.rstrip() + "\n"

def process_post(file_path):
    """Fügt Tags-Glossar zu einem Post hinzu (wenn noch nicht vorhanden)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prüfe ob schon ein Tags-Glossar vorhanden ist
    if '## Tags erklärt' in content:
        print(f"⏭️  Überspringe {file_path.name} (hat bereits Tags-Glossar)")
        return False

    # Extrahiere Tags
    tags = extract_tags_from_frontmatter(content)
    if not tags:
        print(f"⚠️  Keine Tags gefunden in {file_path.name}")
        return False

    # Generiere Glossar
    glossary = generate_tag_glossary(tags)

    # Füge Glossar vor dem letzten Footer ein (falls vorhanden)
    # Oder am Ende des Posts
    if content.rstrip().endswith('*'):
        # Footer vorhanden (z.B. "*Dieser Post wurde mit Claude...*")
        lines = content.rstrip().split('\n')

        # Finde die letzte Zeile mit *...*
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith('*') and lines[i].strip().endswith('*'):
                # Füge Glossar davor ein
                lines.insert(i, glossary)
                content = '\n'.join(lines) + '\n'
                break
    else:
        # Kein Footer, füge am Ende hinzu
        content = content.rstrip() + '\n\n' + glossary

    # Schreibe zurück
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ {file_path.name} - Tags-Glossar hinzugefügt ({len(tags)} Tags)")
    return True

def main():
    """Hauptfunktion."""
    posts_dir = Path('content/posts')

    if not posts_dir.exists():
        print("❌ Verzeichnis 'content/posts' nicht gefunden!")
        return

    # Verarbeite alle Markdown-Dateien
    processed = 0
    skipped = 0

    for md_file in sorted(posts_dir.glob('*.md')):
        # Überspringe spezielle Dateien
        if md_file.name.startswith('.'):
            continue
        if md_file.name == '.obsidian-vault-config.md':
            continue

        if process_post(md_file):
            processed += 1
        else:
            skipped += 1

    print(f"\n✨ Fertig! {processed} Posts aktualisiert, {skipped} übersprungen.")

if __name__ == '__main__':
    main()
