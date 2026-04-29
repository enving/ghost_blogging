# Ghost GitHub Publisher

Publish blog posts to Ghost via GitHub Actions. Die einfachste Methode.

## Commands

### CLI (Terminal)

```bash
# Einzelner Post
gh workflow run publish.yml -f post_file=dein-post.md --repo enving/ghost_blogging

# Alle Posts
gh workflow run publish.yml -f publish_all=true --repo enving/ghost_blogging
```

### In diesem Chat

Sag einfach:
- "publish den post XYZ"
- "push den neuen post zu ghost"
- "veröffentliche [dateiname] auf dem blog"

## Voraussetzungen

1. **GitHub CLI installiert**:
   ```bash
   brew install gh  # macOS
   # oder: https://github.com/cli/releases
   ```

2. **GitHub eingeloggt**:
   ```bash
   gh auth login
   ```

3. **Credentials** (einmalig einrichten):
   - GitHub → Settings → Secrets and variables → Actions
   - `GHOST_API_URL`: https://digitalalchemisten.de
   - `GHOST_ADMIN_API_KEY`: id:secret (aus Ghost Admin → Settings → Integrations)

## Workflow Datei

Das Workflow liegt in `.github/workflows/publish.yml` und:
- Liest Credentials aus GitHub Secrets
- Erstellt .env Datei (mit newline-fix)
- Führt `scripts/publish_all_posts.py` aus
- Erstellt Posts als Drafts in Ghost

## Post Format

Posts müssen YAML Frontmatter haben:

```markdown
---
title: Dein Titel
excerpt: Kurze Zusammenfassung für SEO
tags:
  - Self-Hosting Tutorials
  - KI & Automation
meta_title: SEO Titel
meta_description: SEO Beschreibung
featured: false
---

# Hauptüberschrift

Dein Inhalt...
```

## Troubleshooting

| Problem | Lösung |
|--------|--------|
| URL Fehler (digitalalchemiste.de) | GitHub Secret aktualisieren |
| Keine Credentials | Settings → Secrets prüfen |
| Workflow läuft nicht | `gh workflow run publish.yml` |

## Nach dem Publish

Der Post ist als **Draft** in Ghost. Zum Review:
- https://digitalalchemisten.de/ghost/#/posts

Von dort kannst du:
- Noch Änderungen machen
- Formatieren
- Veröffentlichen