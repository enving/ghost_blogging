#!/usr/bin/env python3
"""
Publishes all blog posts from content/posts/ to Ghost as drafts.
"""

import os
import sys
import time
import re
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / ".claude/skills/ghost_api_publisher"))

from ghost_publisher import GhostPublisher


def clean_wikilinks(text):
    """
    Converts [[Link|Text]] to Text and [[Text]] to Text.
    This ensures Ghost (which doesn't support Wikilinks) displays clean text.
    """
    # Pattern for [[Link|Text]]
    text = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", text)
    # Pattern for [[Text]]
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    return text


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Parse YAML-like frontmatter
    metadata = {}
    current_key = None
    current_list = []

    for line in frontmatter_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if ":" in line and not line.startswith("-"):
            if current_key and current_list:
                metadata[current_key] = current_list
                current_list = []

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if value.startswith("[") and value.endswith("]"):
                # Inline-Liste: tags: ["A", "B"] — sonst landet der ganze
                # Ausdruck als ein einziger Tag in Ghost.
                inner = value[1:-1].strip()
                metadata[key] = [
                    v.strip().strip('"').strip("'")
                    for v in inner.split(",")
                    if v.strip()
                ] if inner else []
                current_key = None
            elif value:
                metadata[key] = value
                current_key = None
            else:
                current_key = key
        elif line.startswith("-") and current_key:
            value = line[1:].strip().strip('"').strip("'")
            current_list.append(value)

    if current_key and current_list:
        metadata[current_key] = current_list

    return metadata, body


def main():
    """Main function."""
    # Load credentials from .env (for local testing)
    # In GitHub Actions, these will be set as environment variables from Secrets
    api_url = os.getenv("GHOST_API_URL", "https://digitalalchemisten.de")
    admin_api_key = os.getenv("GHOST_ADMIN_API_KEY")

    if api_url:
        api_url = api_url.rstrip('\n\r')
    if admin_api_key:
        admin_api_key = admin_api_key.rstrip('\n\r')

    if not admin_api_key:
        # Try to read from .env file (for local development)
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("GHOST_ADMIN_API_KEY="):
                        admin_api_key = line.split("=", 1)[1].strip()
                    elif line.startswith("GHOST_API_URL="):
                        api_url = line.split("=", 1)[1].strip()

    if not admin_api_key:
        print("❌ Error: GHOST_ADMIN_API_KEY not found")
        print("   - For local testing: Add to .env file")
        print("   - For GitHub Actions: Configure as Secret")
        return

    # Initialize Ghost publisher
    print("🚀 Initializing Ghost Publisher...\n")
    ghost = GhostPublisher(api_url=api_url, admin_api_key=admin_api_key)

    # Get all markdown files
    posts_dir = Path("content/posts")
    md_files = sorted(posts_dir.glob("*.md"))

    # Filter out special files
    md_files = [f for f in md_files if not f.name.startswith(".")]

    # Restrict to a single post when asked (workflow input / CLI argument).
    only = os.environ.get("POST_FILE", "").strip() or (
        sys.argv[1].strip() if len(sys.argv) > 1 else ""
    )
    if only:
        only_name = Path(only).name
        md_files = [f for f in md_files if f.name == only_name]
        if not md_files:
            print(f"❌ No post named {only_name!r} in {posts_dir}/")
            return 1
        print(f"🎯 Restricted to a single post: {only_name}")

    # Titles already in Ghost — creating them again would duplicate live posts.
    try:
        existing_raw = ghost.get_posts(limit="all").get("posts", [])
        existing = {p.get("title", "").strip().lower() for p in existing_raw}
        print(f"🔍 {len(existing)} posts already in Ghost (checked for duplicates)")
    except Exception as e:
        print(f"❌ Could not read existing posts, aborting to avoid duplicates: {e}")
        return 1

    print(f"📚 Found {len(md_files)} posts to publish\n")
    print("=" * 60)

    published_count = 0
    skipped_count = 0
    failed_count = 0

    for md_file in md_files:
        print(f"\n📝 Processing: {md_file.name}")

        try:
            # Read file
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract frontmatter
            metadata, body = extract_frontmatter(content)

            if not metadata:
                print(f"   ⚠️  No frontmatter found, skipping")
                skipped_count += 1
                continue

            # Prepare post data
            title = metadata.get("title", md_file.stem)
            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]

            excerpt = metadata.get("excerpt", "")
            featured = metadata.get("featured", "false").lower() == "true"

            # Meta fields
            meta_title = metadata.get("meta_title", title)
            meta_description = metadata.get("meta_description", excerpt)

            if title.strip().lower() in existing:
                print(f"   ⏭️  Already in Ghost, skipping: {title}")
                skipped_count += 1
                continue

            print(f"   Title: {title}")
            print(f"   Tags: {', '.join(tags)}")
            print(f"   Featured: {featured}")

            # Create draft
            # Clean wikilinks from body before publishing to Ghost
            clean_body = clean_wikilinks(body)

            result = ghost.create_post(
                title=title,
                markdown_content=clean_body,
                status="draft",
                tags=tags,
                custom_excerpt=excerpt,
                featured=featured,
                visibility="public",
                meta_title=meta_title,
                meta_description=meta_description,
            )

            if result:
                print(f"   ✅ Published as draft!")
                try:
                    if isinstance(result, dict) and "id" in result:
                        post_id = result["id"]
                    elif (
                        isinstance(result, dict)
                        and "posts" in result
                        and len(result["posts"]) > 0
                    ):
                        post_id = result["posts"][0]["id"]
                    else:
                        post_id = "unknown"

                    if post_id != "unknown":
                        print(
                            f"   🔗 Admin URL: {ghost.api_url.replace('/ghost/api/admin', '')}/ghost/#/editor/post/{post_id}"
                        )
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
        print(
            f"🔗 Review them at: {ghost.api_url.replace('/ghost/api/admin', '')}/ghost/#/posts"
        )


if __name__ == "__main__":
    # Propagate failures so the GitHub workflow turns red instead of
    # reporting success after an aborted run.
    sys.exit(main() or 0)
