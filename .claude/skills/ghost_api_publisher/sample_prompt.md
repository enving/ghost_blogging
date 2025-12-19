# Sample Prompts for Ghost API Publisher

## Quick Start

Hey Claude—I just added the "ghost-api-publisher" skill. Can you create a blog post from my markdown file?

## Specific Use Cases

### Use Case 1: Create Draft from Markdown File

I have a markdown file at `content/posts/kubernetes-basics.md`. Can you create a draft blog post from it on Ghost? Add the tags "Kubernetes", "DevOps", and "Für Einsteiger". Set the excerpt to "Lerne Kubernetes Grundlagen in 45 Minuten - praktisch und verständlich erklärt."

### Use Case 2: Publish Existing Draft

Show me all my draft posts in Ghost, then publish the one about "Docker Tutorial" with the meta description "Complete Docker guide for beginners - from installation to deployment in 30 minutes."

### Use Case 3: Update Post Content

I updated the file `content/posts/ghost-setup.md`. Can you update the corresponding Ghost blog post (search for title "Ghost Blog mit Claude verbinden") with the new content? Keep it as a draft for now.

### Use Case 4: Bulk Operations

Fetch all published posts tagged with "Tutorial" and show me their titles and IDs. I want to add the tag "Self-Hosting" to all of them.

### Use Case 5: Create Post from Scratch

Create a new draft blog post with the title "KI-Tools für 2025: Die Top 10 für Non-Techies". Write a short introductory paragraph about how AI tools are becoming more accessible. Add tags "KI & Automation", "Innovation & Tools", and "Für Einsteiger".

## Tips for Best Results

- **Be specific about tags**: Use the standard taxonomy from CLAUDE.md (KI & Automation, Self-Hosting Tutorials, etc.)
- **Always draft first**: Create posts as drafts, review in Ghost Admin UI, then publish
- **Include SEO metadata**: Mention if you want custom meta_title, meta_description, or excerpt
- **Reference files clearly**: Use full paths like `content/posts/filename.md`
- **Batch operations**: You can ask Claude to perform multiple operations in sequence
