#!/usr/bin/env python3
"""
Upload the Knowledge Graphs for Verwaltung blog post to Ghost as a draft.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import ghost_publisher
sys.path.insert(0, str(Path(__file__).parent))

from ghost_publisher import GhostPublisher
from dotenv import load_dotenv

def main():
    # Load environment variables from .env in repository root
    repo_root = Path(__file__).parent.parent.parent.parent
    env_path = repo_root / '.env'

    if not env_path.exists():
        print(f"❌ Error: .env file not found at {env_path}")
        return 1

    load_dotenv(env_path)

    # Get Ghost credentials
    api_url = os.getenv('GHOST_API_URL')
    admin_api_key = os.getenv('GHOST_ADMIN_API_KEY')
    api_version = os.getenv('GHOST_API_VERSION', 'v5.0')

    if not api_url or not admin_api_key:
        print("❌ Error: Missing GHOST_API_URL or GHOST_ADMIN_API_KEY in .env")
        return 1

    # Read the markdown file
    post_path = repo_root / 'content' / 'posts' / '2025-01-verwaltung-ki-knowledge-graphs.md'

    if not post_path.exists():
        print(f"❌ Error: Post file not found at {post_path}")
        return 1

    with open(post_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Extract metadata and content
    # Remove the Ghost Metadata section from the content
    content_parts = markdown_content.split('## Ghost Metadata')
    main_content = content_parts[0].strip()

    # Extract title (first line starting with #)
    lines = main_content.split('\n')
    title = lines[0].replace('# ', '').strip()

    # Remove title from content for Ghost (it will be added separately)
    content_without_title = '\n'.join(lines[1:]).strip()

    # Initialize Ghost Publisher
    publisher = GhostPublisher(api_url, admin_api_key, api_version)

    # Convert markdown to HTML
    html_content = publisher.markdown_to_html(content_without_title)

    # Post metadata from the file
    post_data = {
        'title': title,
        'html_content': html_content,
        'status': 'draft',
        'tags': ['KI & Automation', 'Digitale Souveränität', 'Innovation & Tools'],
        'custom_excerpt': 'Können Knowledge Graphs und KI die Verwaltung revolutionieren? Ein Gedankenexperiment: Wie moderne Software-Konzepte Förderanträge vereinfachen könnten – mit echtem Praxis-Test.',
        'meta_title': 'KI & Knowledge Graphs für die Verwaltung - Ein Experiment',
        'meta_description': 'Können KI-Systeme Förderanträge automatisch prüfen? Ein Gedankenexperiment mit Context7, Knowledge Graphs und modernen LLMs – inklusive Praxis-Test.'
    }

    print(f"📝 Creating draft post: {title}")
    print(f"📊 Tags: {', '.join(post_data['tags'])}")
    print(f"🔗 Ghost URL: {api_url}")
    print()

    # Create the draft post
    try:
        result = publisher.create_post(**post_data)

        if result and 'posts' in result:
            post = result['posts'][0]
            post_id = post['id']
            post_url = post.get('url', '')

            print("✅ Draft post created successfully!")
            print(f"📌 Post ID: {post_id}")
            print(f"🔗 Admin URL: {api_url.replace('/ghost/api/admin', '')}/ghost/#/editor/post/{post_id}")
            print(f"🌐 Preview URL: {post_url}")
            print()
            print("Next steps:")
            print("1. Review the draft in Ghost Admin")
            print("2. Add a feature image if desired")
            print("3. Publish when ready")

            return 0
        else:
            print("❌ Error: Unexpected response from Ghost API")
            print(result)
            return 1

    except Exception as e:
        print(f"❌ Error creating post: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
