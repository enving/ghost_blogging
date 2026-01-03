#!/usr/bin/env python3
"""
Fügt automatisch [[Wikilinks]] zu technischen Begriffen in Blog-Posts hinzu.
"""

import re
from pathlib import Path

# Begriffe die wir im Glossar haben
GLOSSARY_TERMS = [
    'MCP', 'Ghost', 'VPS', 'API', 'DSGVO', 'Claude', 'Docker', 'SSH', 'SSL',
    'SEO', 'JWT', 'OAuth', 'CI/CD', 'Node.js', 'Python', 'Markdown', 'YAML',
    'JSON', 'Git', 'GitHub', 'Nginx', 'MySQL', 'Self-Hosting', 'Open Source',
    'KI', 'AI', 'LLM', 'Obsidian', 'Wikilinks', 'Frontmatter'
]

def add_wikilinks_to_content(content, glossary_dir):
    """Fügt Wikilinks zu Begriffen hinzu."""

    # Finde alle existierenden Glossar-Einträge
    existing_glossary = set()
    for md_file in glossary_dir.glob('*.md'):
        term = md_file.stem.replace('-', '/')  # CI-CD → CI/CD
        existing_glossary.add(term)

    modified = False
    lines = content.split('\n')
    new_lines = []

    in_code_block = False
    in_frontmatter = False

    for line in lines:
        # Skip frontmatter
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            new_lines.append(line)
            continue

        if in_frontmatter:
            new_lines.append(line)
            continue

        # Skip code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            new_lines.append(line)
            continue

        # Skip bereits vorhandene Wikilinks
        if '[[' in line and ']]' in line:
            new_lines.append(line)
            continue

        # Füge Wikilinks hinzu
        new_line = line
        for term in sorted(existing_glossary, key=len, reverse=True):  # Längste zuerst
            # Pattern: Wort boundary, Begriff, Wort boundary
            # Aber nicht in bereits existierenden Wikilinks
            pattern = r'\b(' + re.escape(term) + r')\b'

            # Prüfe ob dieser Begriff im Line vorkommt
            if re.search(pattern, new_line, re.IGNORECASE):
                # Ersetze nur die erste Erwähnung pro Absatz
                new_line = re.sub(
                    pattern,
                    r'[[\1]]',
                    new_line,
                    count=1,  # Nur erste Erwähnung
                    flags=re.IGNORECASE
                )
                modified = True

        new_lines.append(new_line)

    return '\n'.join(new_lines), modified

def process_post(file_path, glossary_dir, dry_run=False):
    """Verarbeitet einen Post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, modified = add_wikilinks_to_content(content, glossary_dir)

    if modified:
        if dry_run:
            print(f"   ⚠️  Würde ändern (Dry-Run)")
            return False
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"   ✅ Wikilinks hinzugefügt")
            return True
    else:
        print(f"   ⏭️  Keine Änderungen nötig")
        return False

def main(dry_run=False):
    """Main function."""
    posts_dir = Path('content/posts')
    glossary_dir = Path('content/glossar')

    if not glossary_dir.exists():
        print("❌ Glossar-Verzeichnis nicht gefunden!")
        return

    print(f"🔍 Füge Wikilinks zu technischen Begriffen hinzu...")
    if dry_run:
        print("⚠️  DRY-RUN Modus (keine Änderungen)\n")
    else:
        print()

    print("=" * 60)

    modified_count = 0
    skipped_count = 0

    for md_file in sorted(posts_dir.glob('*.md')):
        if md_file.name.startswith('.'):
            continue

        print(f"\n📝 {md_file.name}")

        if process_post(md_file, glossary_dir, dry_run):
            modified_count += 1
        else:
            skipped_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("\n📊 ZUSAMMENFASSUNG:")
    print(f"   ✅ Geändert: {modified_count}")
    print(f"   ⏭️  Unverändert: {skipped_count}")

    if dry_run:
        print("\n💡 Führe ohne --dry-run aus, um Änderungen zu speichern")

if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    main(dry_run=dry_run)
