#!/usr/bin/env python3
"""
Example script to publish a markdown file to Ghost as a blog post.
This demonstrates the complete workflow from markdown file to published Ghost post.
"""

import sys
sys.path.insert(0, '.claude/skills/ghost_api_publisher')

import requests
import jwt
import time
import json

# Load credentials from .env
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

# Read markdown file (adjust path as needed)
markdown_file = 'content/posts/YOUR_POST.md'
print(f"📖 Reading markdown file: {markdown_file}")

with open(markdown_file, 'r', encoding='utf-8') as f:
    markdown_content = f.read()

print(f"   Markdown: {len(markdown_content)} characters")

# Create Lexical format with markdown card
# This is the correct format for Ghost v5+
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

# Create post with proper settings
print("\n📝 Creating blog post in Ghost...")
post_data = {
    "posts": [{
        "title": "YOUR POST TITLE",
        "lexical": json.dumps(lexical_data),
        "status": "draft",  # Use "published" to publish immediately
        "featured": False,  # Set to True to feature on homepage
        "visibility": "public",  # Options: "public", "members", "paid"
        "tags": ["Tag 1", "Tag 2", "Tag 3"],  # Your tags here
        "custom_excerpt": "Short description for listings and SEO",
        "meta_title": "SEO Title (optional, defaults to title)",
        "meta_description": "SEO description for search engines",
        "og_title": "Social media title (optional)",
        "og_description": "Social media description (optional)"
    }]
}

response = requests.post(f"{API_URL}/posts/", json=post_data, headers=headers)

if response.status_code == 201:
    result = response.json()
    post = result['posts'][0]

    print(f"\n✅ Post successfully created!")
    print(f"\n📋 Post Details:")
    print(f"   Title: {post['title']}")
    print(f"   Status: {post['status']}")
    print(f"   Featured: {post['featured']}")
    print(f"   Visibility: {post['visibility']}")
    print(f"   Tags: {[tag['name'] for tag in post.get('tags', [])]}")
    print(f"\n🔗 Links:")
    print(f"   Ghost Admin: https://yourdomain.com/ghost/#/editor/post/{post['id']}")
    print(f"   Preview: https://yourdomain.com/p/{post['uuid']}/")

else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.text)
