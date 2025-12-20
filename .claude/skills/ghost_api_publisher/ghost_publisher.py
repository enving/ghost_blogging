"""
Ghost Blog Publisher - Create and manage blog posts via Ghost Admin API.

This script handles authentication, Markdown-to-Lexical conversion (Ghost v5+),
and post creation/updates through the Ghost Admin API.

IMPORTANT: Ghost v5+ uses Lexical format, not HTML!
"""

import requests
import jwt
import time
import json
from typing import Dict, Optional, List
from pathlib import Path


class GhostPublisher:
    """Handles Ghost Admin API interactions for blog post management."""

    def __init__(self, api_url: str, admin_api_key: str, api_version: str = "v5.0"):
        """
        Initialize Ghost Publisher.

        Args:
            api_url: Base URL of Ghost instance (e.g., https://yourdomain.com)
            admin_api_key: Admin API key from Ghost integration (format: id:secret)
            api_version: Ghost API version (default: v5.0)
        """
        self.api_url = api_url.rstrip('/') + '/ghost/api/admin'
        self.api_version = api_version

        # Split API key
        try:
            self.key_id, self.key_secret = admin_api_key.split(':')
        except ValueError:
            raise ValueError("Admin API key must be in format 'id:secret'")

    def _generate_jwt_token(self) -> str:
        """
        Generate JWT token for Ghost Admin API authentication.

        Returns:
            JWT token string valid for 5 minutes
        """
        iat = int(time.time())

        header = {
            'alg': 'HS256',
            'typ': 'JWT',
            'kid': self.key_id
        }

        payload = {
            'iat': iat,
            'exp': iat + 300,  # Token expires in 5 minutes
            'aud': '/admin/'
        }

        token = jwt.encode(
            payload,
            bytes.fromhex(self.key_secret),
            algorithm='HS256',
            headers=header
        )

        return token

    def _get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers for API requests.

        Returns:
            Dictionary with Authorization and Content-Type headers
        """
        token = self._generate_jwt_token()

        return {
            'Authorization': f'Ghost {token}',
            'Content-Type': 'application/json',
            'Accept-Version': self.api_version
        }

    def markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown to HTML using markdown library.

        Args:
            markdown_content: Markdown text to convert

        Returns:
            HTML string
        """
        try:
            import markdown
            html = markdown.markdown(
                markdown_content,
                extensions=['extra', 'codehilite', 'fenced_code', 'tables']
            )
            return html
        except ImportError:
            # Fallback: Basic conversion if markdown library not available
            print("Warning: markdown library not installed. Using basic conversion.")
            html = markdown_content
            html = html.replace('\n\n', '</p><p>')
            html = html.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
            html = html.replace('## ', '<h2>').replace('\n', '</h2>\n')
            html = html.replace('```', '<pre><code>').replace('```', '</code></pre>')
            html = f'<p>{html}</p>'
            return html

    def create_post(
        self,
        title: str,
        markdown_content: str,
        status: str = "draft",
        tags: Optional[List[str]] = None,
        custom_excerpt: Optional[str] = None,
        meta_title: Optional[str] = None,
        meta_description: Optional[str] = None,
        feature_image: Optional[str] = None,
        featured: bool = False,
        visibility: str = "public"
    ) -> Dict:
        """
        Create a new blog post in Ghost using Lexical format (Ghost v5+).

        Args:
            title: Post title
            markdown_content: Post content in Markdown format
            status: Post status ('draft' or 'published')
            tags: List of tag names
            custom_excerpt: Short excerpt for post listings
            meta_title: SEO title (defaults to title)
            meta_description: SEO description
            feature_image: URL to feature image
            featured: Set to True to feature post on homepage
            visibility: 'public', 'members', or 'paid'

        Returns:
            Response dictionary with post data
        """
        # Create Lexical format with markdown card (Ghost v5+ compatible)
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

        post_data = {
            "posts": [{
                "title": title,
                "lexical": json.dumps(lexical_data),
                "status": status,
                "featured": featured,
                "visibility": visibility
            }]
        }

        # Add optional fields if provided
        post = post_data["posts"][0]
        if tags:
            post["tags"] = tags
        if custom_excerpt:
            post["custom_excerpt"] = custom_excerpt
        if meta_title:
            post["meta_title"] = meta_title
        if meta_description:
            post["meta_description"] = meta_description
        if feature_image:
            post["feature_image"] = feature_image

        headers = self._get_headers()
        response = requests.post(
            f"{self.api_url}/posts/",
            json=post_data,
            headers=headers
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create post: {response.status_code} - {response.text}")

    def update_post(
        self,
        post_id: str,
        updated_at: str,
        title: Optional[str] = None,
        markdown_content: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_excerpt: Optional[str] = None,
        meta_title: Optional[str] = None,
        meta_description: Optional[str] = None,
        featured: Optional[bool] = None,
        visibility: Optional[str] = None
    ) -> Dict:
        """
        Update an existing blog post using Lexical format (Ghost v5+).

        Args:
            post_id: ID of the post to update
            updated_at: Timestamp from original post (for conflict prevention)
            title: New title (optional)
            markdown_content: New Markdown content (optional)
            status: New status (optional)
            tags: New tags list (optional)
            custom_excerpt: New excerpt (optional)
            meta_title: New SEO title (optional)
            meta_description: New SEO description (optional)
            featured: Set featured status (optional)
            visibility: New visibility setting (optional)

        Returns:
            Response dictionary with updated post data
        """
        update_data = {
            "posts": [{
                "updated_at": updated_at
            }]
        }

        # Add fields to update
        post = update_data["posts"][0]
        if title:
            post["title"] = title
        if markdown_content:
            # Convert to Lexical format
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
            post["lexical"] = json.dumps(lexical_data)
        if status:
            post["status"] = status
        if tags is not None:
            post["tags"] = tags
        if custom_excerpt:
            post["custom_excerpt"] = custom_excerpt
        if meta_title:
            post["meta_title"] = meta_title
        if meta_description:
            post["meta_description"] = meta_description
        if featured is not None:
            post["featured"] = featured
        if visibility:
            post["visibility"] = visibility

        headers = self._get_headers()
        response = requests.put(
            f"{self.api_url}/posts/{post_id}/",
            json=update_data,
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update post: {response.status_code} - {response.text}")

    def get_posts(
        self,
        filter_status: Optional[str] = None,
        limit: int = 15,
        include: Optional[str] = None
    ) -> Dict:
        """
        Get posts from Ghost.

        Args:
            filter_status: Filter by status ('draft' or 'published')
            limit: Number of posts to retrieve
            include: Additional data to include (e.g., 'tags,authors')

        Returns:
            Response dictionary with posts data
        """
        headers = self._get_headers()

        params = {
            'limit': limit
        }
        if filter_status:
            params['filter'] = f'status:{filter_status}'
        if include:
            params['include'] = include

        response = requests.get(
            f"{self.api_url}/posts/",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get posts: {response.status_code} - {response.text}")

    def get_post_by_id(self, post_id: str, include: Optional[str] = None) -> Dict:
        """
        Get a single post by ID.

        Args:
            post_id: ID of the post
            include: Additional data to include

        Returns:
            Response dictionary with post data
        """
        headers = self._get_headers()

        params = {}
        if include:
            params['include'] = include

        response = requests.get(
            f"{self.api_url}/posts/{post_id}/",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get post: {response.status_code} - {response.text}")

    def delete_post(self, post_id: str) -> bool:
        """
        Delete a post.

        Args:
            post_id: ID of the post to delete

        Returns:
            True if successful
        """
        headers = self._get_headers()

        response = requests.delete(
            f"{self.api_url}/posts/{post_id}/",
            headers=headers
        )

        if response.status_code == 204:
            return True
        else:
            raise Exception(f"Failed to delete post: {response.status_code} - {response.text}")

    @classmethod
    def from_env_file(cls, env_file_path: str = ".env") -> "GhostPublisher":
        """
        Create GhostPublisher instance from .env file.

        Args:
            env_file_path: Path to .env file (default: .env in current directory)

        Returns:
            GhostPublisher instance
        """
        env_vars = {}

        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

        api_url = env_vars.get('GHOST_API_URL')
        admin_key = env_vars.get('GHOST_ADMIN_API_KEY')
        api_version = env_vars.get('GHOST_API_VERSION', 'v5.0')

        if not api_url or not admin_key:
            raise ValueError("GHOST_API_URL and GHOST_ADMIN_API_KEY must be set in .env file")

        return cls(api_url, admin_key, api_version)


def main():
    """Example usage of GhostPublisher."""

    # Load from .env file
    publisher = GhostPublisher.from_env_file()

    # Example 1: Create a draft post
    print("Creating draft post...")
    result = publisher.create_post(
        title="Test Post from Python Script",
        html_content="<p>This is a test post created using the GhostPublisher class.</p>",
        status="draft",
        tags=["Test", "API"],
        custom_excerpt="A test post to demonstrate the Ghost API integration."
    )

    post_id = result['posts'][0]['id']
    print(f"✅ Post created with ID: {post_id}")

    # Example 2: Get all draft posts
    print("\nFetching draft posts...")
    drafts = publisher.get_posts(filter_status='draft')
    print(f"Found {len(drafts['posts'])} draft posts")

    # Example 3: Update the post
    print(f"\nUpdating post {post_id}...")
    updated_at = result['posts'][0]['updated_at']
    publisher.update_post(
        post_id=post_id,
        updated_at=updated_at,
        html_content="<p>This post has been updated!</p><p>New content added.</p>"
    )
    print("✅ Post updated")


if __name__ == "__main__":
    main()
