#!/usr/bin/env python3
"""
Publishes all blog posts from content/posts/ to Ghost as drafts.
"""

import os
import sys
import time
from pathlib import Path

# Add skill directory to path
sys.path.insert(0, str(Path(__file__).parent / '.claude/skills/ghost_api_publisher'))

from ghost_publisher import GhostPublisher

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Parse YAML-like frontmatter
    metadata = {}
    current_key = None
    current_list = []

    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        if ':' in line and not line.startswith('-'):
            if current_key and current_list:
                metadata[current_key] = current_list
                current_list = []

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if value:
                metadata[key] = value
                current_key = None
            else:
                current_key = key
        elif line.startswith('-') and current_key:
            value = line[1:].strip().strip('"').strip("'")
            current_list.append(value)

    if current_key and current_list:
        metadata[current_key] = current_list

    return metadata, body

def main():
    """Main function."""
    # Load credentials from .env
    api_url = os.getenv('GHOST_API_URL', 'https://digitalalchemisten.de')
    admin_api_key = os.getenv('GHOST_ADMIN_API_KEY')

    if not admin_api_key:
        # Try to read from .env file
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('GHOST_ADMIN_API_KEY='):
                        admin_api_key = line.split('=', 1)[1].strip()
                    elif line.startswith('GHOST_API_URL='):
                        api_url = line.split('=', 1)[1].strip()

    if not admin_api_key:
        print("❌ Error: GHOST_ADMIN_API_KEY not found in .env file")
        return

    # Initialize Ghost publisher
    print("🚀 Initializing Ghost Publisher...\n")
    ghost = GhostPublisher(api_url=api_url, admin_api_key=admin_api_key)

    # Get all markdown files
    posts_dir = Path('content/posts')
    md_files = sorted(posts_dir.glob('*.md'))

    # Filter out special files
    md_files = [f for f in md_files if not f.name.startswith('.')]

    print(f"📚 Found {len(md_files)} posts to publish\n")
    print("=" * 60)

    published_count = 0
    skipped_count = 0
    failed_count = 0

    for md_file in md_files:
        print(f"\n📝 Processing: {md_file.name}")

        try:
            # Read file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            metadata, body = extract_frontmatter(content)

            if not metadata:
                print(f"   ⚠️  No frontmatter found, skipping")
                skipped_count += 1
                continue

            # Prepare post data
            title = metadata.get('title', md_file.stem)
            tags = metadata.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]

            excerpt = metadata.get('excerpt', '')
            featured = metadata.get('featured', 'false').lower() == 'true'

            # Meta fields
            meta_title = metadata.get('meta_title', title)
            meta_description = metadata.get('meta_description', excerpt)

            print(f"   Title: {title}")
            print(f"   Tags: {', '.join(tags)}")
            print(f"   Featured: {featured}")

            # Create draft
            result = ghost.create_post(
                title=title,
                markdown_content=body,
                status='draft',
                tags=tags,
                custom_excerpt=excerpt,
                featured=featured,
                visibility='public',
                meta_title=meta_title,
                meta_description=meta_description
            )

            if result:
                print(f"   ✅ Published as draft!")
                try:
                    if isinstance(result, dict) and 'id' in result:
                        post_id = result['id']
                    elif isinstance(result, dict) and 'posts' in result and len(result['posts']) > 0:
                        post_id = result['posts'][0]['id']
                    else:
                        post_id = 'unknown'

                    if post_id != 'unknown':
                        print(f"   🔗 Admin URL: {ghost.api_url.replace('/ghost/api/admin', '')}/ghost/#/editor/post/{post_id}")
                except Exception as e:
                    print(f"   ⚠️  Could not generate URL: {e}")

                published_count += 1

                # Small delay to avoid rate limiting
                time.sleep(1)
            else:
                print(f"   ❌ Failed to publish")
                failed_count += 1

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("\n📊 SUMMARY")
    print(f"   ✅ Published: {published_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📝 Total: {len(md_files)}")

    if published_count > 0:
        print(f"\n🎉 All posts are now in Ghost as drafts!")
        print(f"🔗 Review them at: {ghost.api_url.replace('/ghost/api/admin', '')}/ghost/#/posts")

if __name__ == '__main__':
    main()
