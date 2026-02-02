#!/usr/bin/env python3
"""
Generate Metadata für Claude-Zugriff

Scannt content/posts/ und erstellt JSON-Metadaten
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, Tuple

# Konfiguration
BASE_DIR = Path(__file__).parent.parent
POSTS_DIR = BASE_DIR / "content/posts"
METADATA_DIR = BASE_DIR / "data/metadata"
METADATA_DIR.mkdir(exist_ok=True)

def extract_frontmatter(md_file: Path) -> Tuple[Dict, str]:
    """Extrahiert YAML Frontmatter"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️  Fehler: {md_file.name}: {e}")
        return {}, ""

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content

    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except:
        frontmatter = {}

    return frontmatter, match.group(2)

def slugify(text: str) -> str:
    """Text → URL-Slug"""
    text = text.lower()
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def generate_posts_index() -> Dict:
    """Scannt Posts und erstellt Index"""
    posts_index = {}

    for md_file in POSTS_DIR.glob("*.md"):
        frontmatter, body = extract_frontmatter(md_file)

        title = frontmatter.get('title', md_file.stem)
        slug = frontmatter.get('slug') or slugify(title)

        # Links extrahieren
        wikilinks = re.findall(r'\[\[(.*?)\]\]', body)
        regular_links = re.findall(r'\[.*?\]\((\/[^\)]+)\)', body)

        posts_index[slug] = {
            'title': title,
            'file': md_file.name,
            'date': str(frontmatter.get('date', '')),
            'tags': frontmatter.get('tags', []) or [],
            'status': frontmatter.get('status', 'draft'),
            'difficulty': frontmatter.get('difficulty', ''),
            'reading_time': frontmatter.get('reading_time', ''),
            'featured': frontmatter.get('featured', False),
            'excerpt': frontmatter.get('excerpt', ''),
            'related_posts': frontmatter.get('related_posts', []) or [],
            'wikilinks': wikilinks,
            'internal_links': [l for l in regular_links if l.startswith('/')],
        }

    return posts_index

def generate_links_graph(posts_index: Dict) -> Dict:
    """Link-Graph erstellen"""
    nodes = []
    edges = []

    for slug, post in posts_index.items():
        nodes.append({
            'id': slug,
            'title': post['title'],
            'tags': post['tags'],
            'status': post['status']
        })

        # Wikilinks
        for wikilink in post['wikilinks']:
            target = slugify(wikilink)
            if target in posts_index:
                edges.append({'source': slug, 'target': target, 'type': 'wikilink'})

        # Related
        for related in post['related_posts']:
            target = slugify(related)
            if target in posts_index:
                edges.append({'source': slug, 'target': target, 'type': 'related'})

    return {'nodes': nodes, 'edges': edges}

def main():
    print("\n🔄 Generating Metadata from content/posts/\n")

    # Posts
    print("📊 Scanning Posts...")
    posts = generate_posts_index()
    posts_file = METADATA_DIR / "posts_index.json"
    with open(posts_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(posts)} posts → {posts_file.name}\n")

    # Links
    print("🕸️  Building Graph...")
    graph = generate_links_graph(posts)
    graph_file = METADATA_DIR / "links_graph.json"
    with open(graph_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {len(graph['nodes'])} nodes, {len(graph['edges'])} edges → {graph_file.name}\n")

    # Summary
    print("="*60)
    print(f"📝 Posts: {len(posts)}")
    print(f"🕸️  Verbindungen: {len(graph['edges'])}")

    tags = {}
    for post in posts.values():
        for tag in post['tags']:
            tags[tag] = tags.get(tag, 0) + 1

    if tags:
        print(f"\n🏷️  Top Tags:")
        for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {tag}: {count}")

    print("="*60)
    print(f"\n✅ Metadata → {METADATA_DIR}/\n")
    print("💡 Claude kann jetzt darauf zugreifen!")
    print()

if __name__ == "__main__":
    main()
