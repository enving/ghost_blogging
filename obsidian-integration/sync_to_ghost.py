#!/usr/bin/env python3
"""
Obsidian → Ghost Sync Script

Konvertiert Obsidian Markdown-Posts zu Ghost-kompatiblem Format.
Erstellt Metadaten-Index für Claude-Zugriff.
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# === KONFIGURATION ===

BASE_DIR = Path(__file__).parent.parent
OBSIDIAN_VAULT = BASE_DIR / "obsidian-vault"
POSTS_DIR = OBSIDIAN_VAULT / "Posts"
GLOSSARY_DIR = OBSIDIAN_VAULT / "Glossar"

METADATA_DIR = BASE_DIR / "metadata"
METADATA_DIR.mkdir(exist_ok=True)

GHOST_URL = os.getenv("GHOST_API_URL", "http://localhost:2368")
GHOST_ADMIN_KEY = os.getenv("GHOST_ADMIN_API_KEY")

# === HELPER FUNCTIONS ===

def extract_frontmatter(md_file: Path) -> Tuple[Dict, str]:
    """Extrahiert YAML Frontmatter und Content"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️  Fehler beim Lesen von {md_file}: {e}")
        return {}, ""

    # Match ---\n...\n---
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content

    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"⚠️  YAML-Fehler in {md_file}: {e}")
        frontmatter = {}

    body = match.group(2)

    return frontmatter, body


def slugify(text: str) -> str:
    """Konvertiert Text zu URL-Slug"""
    text = text.lower()
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = text.strip('-')
    return text


def convert_wikilinks(content: str, posts_index: Dict) -> str:
    """Konvertiert [[Wikilinks]] zu Markdown-Links"""

    def replace_link(match):
        link_text = match.group(1)

        # Suche Post mit diesem Titel
        for slug, post in posts_index.items():
            if post['title'].lower() == link_text.lower():
                return f'[{link_text}](/{slug})'

        # Fallback: Slugify
        slug = slugify(link_text)
        return f'[{link_text}](/{slug})'

    return re.sub(r'\[\[(.*?)\]\]', replace_link, content)


def generate_posts_index() -> Dict:
    """Scannt Obsidian Vault und erstellt Posts-Index"""

    posts_index = {}

    if not POSTS_DIR.exists():
        print(f"⚠️  Posts-Verzeichnis nicht gefunden: {POSTS_DIR}")
        return posts_index

    for md_file in POSTS_DIR.glob("**/*.md"):
        # Skip drafts folder (später separat behandeln)
        if "drafts" in md_file.parts:
            continue

        frontmatter, body = extract_frontmatter(md_file)

        title = frontmatter.get('title', md_file.stem)
        if not title or title == "":
            title = md_file.stem

        slug = frontmatter.get('ghost_slug') or slugify(title)

        # Extrahiere interne Links
        wikilinks = re.findall(r'\[\[(.*?)\]\]', body)
        regular_links = re.findall(r'\[.*?\]\((\/[^\)]+)\)', body)

        posts_index[slug] = {
            'title': title,
            'file': str(md_file.relative_to(BASE_DIR)),
            'date': str(frontmatter.get('date', '')),
            'tags': frontmatter.get('tags', []) or [],
            'status': frontmatter.get('status', 'draft'),
            'difficulty': frontmatter.get('difficulty', 'einsteiger'),
            'reading_time': frontmatter.get('reading_time', ''),
            'featured': frontmatter.get('featured', False),
            'excerpt': frontmatter.get('excerpt', ''),
            'related_posts': frontmatter.get('related_posts', []) or [],
            'wikilinks': wikilinks,
            'internal_links': [link for link in regular_links if link.startswith('/')],
            'ghost_published': frontmatter.get('ghost_published', False)
        }

    return posts_index


def generate_links_graph(posts_index: Dict) -> Dict:
    """Erstellt Link-Graph für Visualisierung"""

    nodes = []
    edges = []

    for slug, post in posts_index.items():
        nodes.append({
            'id': slug,
            'title': post['title'],
            'tags': post['tags'],
            'status': post['status'],
            'difficulty': post['difficulty']
        })

        # Wikilinks → Edges
        for wikilink in post['wikilinks']:
            target_slug = slugify(wikilink)
            if target_slug in posts_index:
                edges.append({
                    'source': slug,
                    'target': target_slug,
                    'type': 'wikilink'
                })

        # Related Posts → Edges
        for related in post['related_posts']:
            related_slug = slugify(related)
            if related_slug in posts_index:
                edges.append({
                    'source': slug,
                    'target': related_slug,
                    'type': 'related'
                })

    return {'nodes': nodes, 'edges': edges}


def generate_glossary_index() -> Dict:
    """Scannt Glossar-Ordner und erstellt Index"""

    glossary = {}

    if not GLOSSARY_DIR.exists():
        print(f"⚠️  Glossar-Verzeichnis nicht gefunden: {GLOSSARY_DIR}")
        return glossary

    for md_file in GLOSSARY_DIR.glob("*.md"):
        term = md_file.stem

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Fehler beim Lesen von {md_file}: {e}")
            continue

        # Erste Zeile als Definition (nach # entfernen)
        lines = content.strip().split('\n')
        definition = lines[0].strip('#').strip() if lines else ""

        # Falls erster Absatz besser ist:
        if not definition or len(definition) < 10:
            paragraphs = content.split('\n\n')
            if paragraphs:
                definition = paragraphs[0].strip('#').strip()

        glossary[term] = {
            'definition': definition,
            'file': str(md_file.relative_to(BASE_DIR)),
            'url': f'/glossar#{slugify(term)}'
        }

    return glossary


def generate_tags_hierarchy(posts_index: Dict) -> Dict:
    """Analysiert Tags und erstellt Hierarchie"""

    all_tags = {}

    for post in posts_index.values():
        for tag in post['tags']:
            if '/' in tag:
                # Hierarchical tag
                parts = tag.split('/')
                parent = parts[0].strip()
                child = parts[1].strip() if len(parts) > 1 else None

                if parent not in all_tags:
                    all_tags[parent] = {'count': 0, 'children': {}}

                all_tags[parent]['count'] += 1

                if child:
                    if child not in all_tags[parent]['children']:
                        all_tags[parent]['children'][child] = 0
                    all_tags[parent]['children'][child] += 1
            else:
                # Flat tag
                if tag not in all_tags:
                    all_tags[tag] = {'count': 0, 'children': {}}
                all_tags[tag]['count'] += 1

    return all_tags


def print_summary(posts_index: Dict, links_graph: Dict, glossary: Dict):
    """Gibt Zusammenfassung aus"""

    print("\n" + "="*60)
    print("📊 METADATA SUMMARY")
    print("="*60 + "\n")

    print(f"📝 Posts:          {len(posts_index)}")
    print(f"🕸️  Connections:    {len(links_graph['edges'])}")
    print(f"📖 Glossar-Begriffe: {len(glossary)}")

    # Status-Verteilung
    status_count = {}
    for post in posts_index.values():
        status = post['status']
        status_count[status] = status_count.get(status, 0) + 1

    print(f"\n📌 Status:")
    for status, count in status_count.items():
        print(f"   {status}: {count}")

    # Top Tags
    tag_count = {}
    for post in posts_index.values():
        for tag in post['tags']:
            tag_count[tag] = tag_count.get(tag, 0) + 1

    if tag_count:
        print(f"\n🏷️  Top Tags:")
        sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:5]
        for tag, count in sorted_tags:
            print(f"   {tag}: {count}")

    print("\n" + "="*60 + "\n")


# === MAIN FUNCTION ===

def main():
    print("\n🔄 Obsidian → Ghost Metadata Sync\n")

    # 1. Generate Posts Index
    print("📊 Scanning Posts...")
    posts_index = generate_posts_index()

    if not posts_index:
        print("⚠️  Keine Posts gefunden!")
        print(f"   Prüfe: {POSTS_DIR}")
        return

    posts_index_file = METADATA_DIR / "posts_index.json"
    with open(posts_index_file, 'w', encoding='utf-8') as f:
        json.dump(posts_index, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(posts_index)} posts → {posts_index_file}\n")

    # 2. Generate Links Graph
    print("🕸️  Building Links Graph...")
    links_graph = generate_links_graph(posts_index)
    links_graph_file = METADATA_DIR / "links_graph.json"
    with open(links_graph_file, 'w', encoding='utf-8') as f:
        json.dump(links_graph, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(links_graph['nodes'])} nodes, {len(links_graph['edges'])} edges → {links_graph_file}\n")

    # 3. Generate Glossary Index
    print("📖 Indexing Glossary...")
    glossary = generate_glossary_index()
    glossary_file = METADATA_DIR / "glossary_index.json"
    with open(glossary_file, 'w', encoding='utf-8') as f:
        json.dump(glossary, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(glossary)} terms → {glossary_file}\n")

    # 4. Generate Tags Hierarchy
    print("🏷️  Analyzing Tags...")
    tags_hierarchy = generate_tags_hierarchy(posts_index)
    tags_file = METADATA_DIR / "tags_hierarchy.json"
    with open(tags_file, 'w', encoding='utf-8') as f:
        json.dump(tags_hierarchy, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Tags hierarchy → {tags_file}\n")

    # Summary
    print_summary(posts_index, links_graph, glossary)

    print("✅ Metadata sync complete!")
    print(f"\n📁 Metadata saved to: {METADATA_DIR}/")
    print("\n💡 Claude kann jetzt auf diese Metadaten zugreifen:")
    print("   - posts_index.json    → Alle Posts + Details")
    print("   - links_graph.json    → Verbindungen visualisieren")
    print("   - glossary_index.json → Begriffe definieren")
    print("   - tags_hierarchy.json → Tag-Struktur")
    print()


if __name__ == "__main__":
    main()
