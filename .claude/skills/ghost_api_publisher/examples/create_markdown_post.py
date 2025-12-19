import sys
sys.path.insert(0, '.claude/skills/ghost_api_publisher')

import requests
import jwt
import time
import json

# Load from .env
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('GHOST_API_URL='):
            API_URL = line.split('=', 1)[1].strip() + '/ghost/api/admin'
        elif line.startswith('GHOST_ADMIN_API_KEY='):
            API_KEY = line.split('=', 1)[1].strip()

key_id, key_secret = API_KEY.split(':')

# Generate JWT
iat = int(time.time())
token = jwt.encode(
    {'iat': iat, 'exp': iat + 300, 'aud': '/admin/'},
    bytes.fromhex(key_secret),
    algorithm='HS256',
    headers={'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
)

headers = {
    'Authorization': f'Ghost {token}',
    'Content-Type': 'application/json',
    'Accept-Version': 'v5.0'
}

# Read markdown
print("📖 Lese Markdown-Datei...")
with open('content/posts/2025-12-ghost-blog-mit-claude-verbinden.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print(f"   Markdown: {len(markdown_content)} Zeichen")

# Create Lexical with a MARKDOWN CARD instead of text nodes
# Ghost's Lexical uses special "markdown" type nodes for markdown content
lexical_data = {
    "root": {
        "children": [
            {
                "type": "markdown",
                "version": 1,
                "markdown": markdown_content
            }
        ],
        "direction": "ltr",
        "format": "",
        "indent": 0,
        "type": "root",
        "version": 1
    }
}

# Delete old post
old_post_id = "694439cfdf2eb87ea2bd318a"
print(f"\n🗑️ Lösche alten Post {old_post_id}...")
try:
    requests.delete(f"{API_URL}/posts/{old_post_id}/", headers=headers)
    print("   ✅ Gelöscht")
except:
    print("   ⚠️ Konnte nicht löschen")

# Create the post with markdown card
print("\n📝 Erstelle Post mit Markdown-Card...")
post_data = {
    "posts": [{
        "title": "Ghost Blog mit Claude verbinden: Die komplette Anleitung für Einsteiger",
        "lexical": json.dumps(lexical_data),
        "status": "draft",
        "tags": ["Self-Hosting Tutorials", "Für Einsteiger", "KI & Automation"],
        "custom_excerpt": "Eine vollständige Schritt-für-Schritt-Anleitung, wie du deinen eigenen Ghost Blog auf einem VPS einrichtest und mit Claude für automatisierte Content-Erstellung verbindest.",
        "meta_title": "Ghost Blog mit Claude verbinden - Komplette Anleitung",
        "meta_description": "Lerne, wie du deinen eigenen Ghost Blog auf einem VPS (IONOS/Hetzner) einrichtest, SSL konfigurierst und mit Claude über die Admin API verbindest. Inkl. Troubleshooting."
    }]
}

response = requests.post(f"{API_URL}/posts/", json=post_data, headers=headers)

if response.status_code == 201:
    result = response.json()
    post_id = result['posts'][0]['id']
    uuid = result['posts'][0]['uuid']
    
    print(f"\n✅ Post mit Markdown-Card erstellt!")
    print(f"\n📋 Links:")
    print(f"   Ghost Admin: https://digitalalchemisten.de/ghost/#/editor/post/{post_id}")
    print(f"   Preview: https://digitalalchemisten.de/p/{uuid}/")
    print(f"\n🎉 Ghost sollte das Markdown jetzt richtig rendern!")
    
else:
    print(f"\n❌ Fehler: {response.status_code}")
    print(response.text)

