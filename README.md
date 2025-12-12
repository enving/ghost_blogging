# Digitalalchemisten - Technologie verständlich gemacht

Ein praxisorientierter Tech-Blog, der komplexe Themen rund um KI, digitale Souveränität und Innovation für Non-Techies zugänglich macht.

**Domain**: digitalalchemisten.de
**Blog-Titel**: Digitalalchemisten

## 🎯 Mission

Erfahrungen mit digitalen Tools und KI teilen, sodass auch nicht-technische Menschen die spannenden Entwicklungen nachvollziehen und selbst ausprobieren können.

## 🚀 Setup

### Lokal entwickeln

```bash
# Ghost mit Docker starten
docker run -d --name ghost-local -p 2368:2368 -e NODE_ENV=development -v ghost-content:/var/lib/ghost/content ghost:latest

# Blog: http://localhost:2368
# Admin: http://localhost:2368/ghost
```

### Content-Workflow (Token-sparend!)

1. Posts als Markdown-Files in `/content/posts/` schreiben
2. Via Ghost Admin UI importieren
3. Reviewen & veröffentlichen

## 📂 Repository-Struktur

```
ghost-blog/
├── .github/
│   └── workflows/       # CI/CD Pipeline
├── content/
│   ├── posts/          # Markdown Blog-Posts
│   ├── drafts/         # Entwürfe
│   ├── themes/         # Custom Theme
│   └── images/         # Media Files
├── CLAUDE.md           # Projektplan & Dokumentation
└── README.md
```

## 🔧 Technologie-Stack

- **Ghost CMS** (Docker)
- **Node.js** v22+
- **GitHub** für Version Control
- **GitHub Actions** für CI/CD
- **Claude** für Content-Automatisierung

## 📝 Content-Kategorien

- 🤖 KI & Automation
- 🇪🇺 Digitale Souveränität
- 🔧 Self-Hosting Tutorials
- 💡 Innovation & Tools
- 🛡️ Privacy & Security
- 📚 Für Einsteiger

## 🗓️ Projektphase

**Phase 0**: Lokales Development Setup (aktuell)
- ✅ Ghost läuft lokal
- ✅ GitHub-Repository erstellt
- 🔄 Content-Erstellung

**Next Steps**:
- VPS bei IONOS bestellen
- Domain registrieren
- CI/CD Pipeline einrichten

---

**Erstellt**: 2025-12-12
**Status**: In Development
