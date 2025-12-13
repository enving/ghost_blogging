# Digitalalchemisten - Setup Guide

## 📦 Was ist hier drin?

Dieses Repository enthält alles für den **Digitalalchemisten Blog** - ein selbstgehostetes Ghost-Blog mit Claude-Automatisierung.

**Status**: Phase 0 abgeschlossen ✅ (Lokal), Phase 1 bereit 🚀 (VPS-Deployment)

---

## 🚀 Quick Start

### Voraussetzungen

- **Node.js** v22+ (LTS)
- **Docker Desktop** (für lokales Ghost)
- **Git**
- **VPS-Server** (IONOS VPS S empfohlen, 2€/Monat)
- **Domain** (digitalalchemisten.de bereits registriert)

### 1. Repository klonen

```bash
git clone https://github.com/enving/ghost_blogging.git
cd ghost_blogging
```

### 2. Lokales Ghost starten

```bash
# Ghost via Docker
docker run -d \
  --name ghost-local \
  -p 2368:2368 \
  -e NODE_ENV=development \
  -v ghost-content:/var/lib/ghost/content \
  ghost:latest

# Blog öffnen
# Frontend: http://localhost:2368
# Admin: http://localhost:2368/ghost
```

### 3. Environment Variables

```bash
# .env.example kopieren
cp .env.example .env

# Werte eintragen
# VPS_IP, ADMIN_EMAIL, etc.
```

---

## 📂 Repository-Struktur

```
ghost_blogging/
├── .claude/
│   └── skills/
│       └── blog-post-writer.md     # Custom Skill für Content
├── content/
│   ├── posts/                      # Blog-Posts (Markdown)
│   ├── drafts/                     # Entwürfe
│   └── images/                     # Media Files
├── CLAUDE.md                       # Vollständiger Projektplan
├── THEME_VORSCHLAG.md              # Theme-Design (Modern Alchemy)
├── VPS_ANLEITUNG.md                # Step-by-Step VPS-Setup
├── vps-setup.sh                    # Automatisches Server-Setup
├── NEXT_STEPS.md                   # Konkrete nächste Schritte
├── .env.example                    # Environment Template
└── README.md                       # Haupt-Dokumentation
```

---

## 🎯 Workflow: Lokales Development

**Token-sparender Ansatz**:

1. **Posts schreiben** (als Markdown in `content/posts/`)
2. **Lokal testen** (in Ghost auf http://localhost:2368)
3. **Git commit** (Versionskontrolle)
4. **Export** (von lokal)
5. **Import** (auf Production Server)

**Ghost MCP Server**: Nur für Automation nutzen, NICHT für normales Content-Writing!

---

## 🚀 VPS-Deployment

### Schritt 1: Server vorbereiten

```bash
# 1. .env mit VPS-IP füllen
# 2. Setup-Script hochladen
scp vps-setup.sh root@YOUR_VPS_IP:/root/

# 3. Auf Server einloggen
ssh root@YOUR_VPS_IP

# 4. Script ausführen
chmod +x /root/vps-setup.sh
./vps-setup.sh
```

### Schritt 2: Ghost installieren

```bash
# Als ghostuser
sudo -i -u ghostuser
cd /var/www/ghost

# Ghost installieren (interaktiv)
ghost install

# Fragen:
# - Blog URL: https://digitalalchemisten.de
# - MySQL: Ja
# - Nginx: Ja
# - SSL: Ja (Let's Encrypt)
# - Email: deine@email.de
```

### Schritt 3: Domain konfigurieren

**DNS A-Record** (bei Domain-Provider):
```
Type: A
Name: @
Value: YOUR_VPS_IP
TTL: 3600
```

**Propagation testen**:
```bash
ping digitalalchemisten.de
# Sollte YOUR_VPS_IP zeigen
```

### Schritt 4: Content importieren

```bash
# Lokal: Export erstellen
# http://localhost:2368/ghost → Settings → Labs → Export

# Production: Import
# https://digitalalchemisten.de/ghost → Settings → Labs → Import
```

**Detaillierte Anleitung**: Siehe `VPS_ANLEITUNG.md`

---

## 📝 Content erstellen

### Mit Blog-Post-Writer Skill

Der Custom Skill ist in `.claude/skills/blog-post-writer.md` definiert.

**Eigenschaften**:
- Persönlicher, storytelling-fokussierter Stil
- Authentisch statt corporate
- Strukturierte Templates für alle Post-Types
- Automatische Quality-Checks

**Beispiel-Posts**:
- `content/posts/2025-01-ghost-blog-setup.md`
- `content/posts/2025-01-claude-mcp-erklaert.md`

### Content-Kategorien

- 🔧 Tutorial
- 💡 Konzept-Erklärung
- 🛠️ Tool-Review
- 📚 Erfahrungsbericht
- ⚡ Quick-Tip

---

## 🎨 Theme: Modern Alchemy

**Design-Konzept** (siehe `THEME_VORSCHLAG.md`):

**Farben**:
- Primary: `#7C3AED` (Alchemy Purple)
- Accent: `#FCD34D` (Gold)
- Background: `#FFFFFF` / Dark: `#0F0E13`

**Features**:
- Dark Mode native
- Reading Progress Bar
- Alchemie-Touch (subtil!)
- Mobile-First
- A11y-optimiert

---

## 🔒 Security

**Server-Level**:
- Firewall (UFW): SSH, HTTP, HTTPS
- Fail2ban (Brute-Force-Schutz)
- Automatische Updates
- SSL/TLS (Let's Encrypt)

**Ghost-Level**:
- Starke Passwörter
- 2FA aktivieren
- Regelmäßige Backups
- Rate-Limiting

**Backup-Strategie**:
```bash
# Automatisch täglich (Cron)
0 3 * * * /home/ghostuser/backup-ghost.sh

# Manuell
cd /var/www/ghost
ghost backup
```

---

## 📊 Monitoring

**Uptime Robot** (kostenlos):
- URL: https://digitalalchemisten.de
- Interval: 5 Min
- Alerts: Email bei Ausfall

**SSL-Rating**:
- Test: https://www.ssllabs.com/ssltest/
- Ziel: A+ Rating

---

## 🛠️ Nützliche Befehle

### Ghost-Management

```bash
cd /var/www/ghost

ghost status       # Status checken
ghost restart      # Neustarten
ghost stop         # Stoppen
ghost start        # Starten
ghost update       # Update installieren
ghost log          # Logs anzeigen
```

### Docker (lokal)

```bash
docker ps                    # Container checken
docker logs ghost-local      # Logs
docker restart ghost-local   # Neustart
docker stop ghost-local      # Stoppen
```

### Git-Workflow

```bash
git status                   # Änderungen checken
git add .                    # Alle Änderungen stagen
git commit -m "message"      # Commit
git push origin main         # Zu GitHub pushen
```

---

## 🗺️ Roadmap

### ✅ Phase 0: Lokales Setup (DONE)
- Ghost läuft lokal
- Repository initialisiert
- Erste Posts geschrieben
- Skills erstellt

### 🔄 Phase 1: VPS-Deployment (CURRENT)
- Server einrichten
- Ghost Production installieren
- Domain verbinden
- SSL aktivieren
- Go Live!

### ⏳ Phase 2: Content & Theme (NEXT)
- 10+ Posts schreiben
- Custom Theme implementieren
- Newsletter einrichten
- Analytics integrieren

### 🚀 Phase 3: Automation (LATER)
- Ghost MCP für Newsletter
- CI/CD Pipeline
- Backup-Automation
- Performance-Optimierung

---

## 💰 Kosten

| Posten | Kosten/Monat |
|--------|--------------|
| VPS S (IONOS) | 2€ |
| Domain | ~1€ |
| SSL (Let's Encrypt) | 0€ |
| Mailgun (Email) | 0€ (bis 5k) |
| **Total** | **~3€** |

Günstiger als Netflix! 🎉

---

## 📚 Wichtige Dokumente

- **CLAUDE.md**: Vollständiger Projektplan & Roadmap
- **VPS_ANLEITUNG.md**: Step-by-Step Server-Setup
- **THEME_VORSCHLAG.md**: Design-Konzept "Modern Alchemy"
- **NEXT_STEPS.md**: Konkrete nächste Schritte
- **.claude/skills/blog-post-writer.md**: Custom Content-Skill

---

## 🤝 Fortsetzen auf anderem Computer

### Computer A → Computer B Übergabe

**1. Repository klonen**:
```bash
git clone https://github.com/enving/ghost_blogging.git
cd ghost_blogging
```

**2. Environment Setup**:
```bash
cp .env.example .env
# VPS_IP und andere Werte eintragen
```

**3. Lokales Ghost starten**:
```bash
docker run -d --name ghost-local -p 2368:2368 \
  -e NODE_ENV=development \
  -v ghost-content:/var/lib/ghost/content ghost:latest
```

**4. Aktuellen Stand checken**:
```bash
# Todos & Status in NEXT_STEPS.md
# VPS-Status testen
ssh root@YOUR_VPS_IP
```

---

## ❓ Troubleshooting

### Ghost startet nicht

```bash
# Logs checken
docker logs ghost-local

# Neu starten
docker restart ghost-local
```

### VPS nicht erreichbar

```bash
# Ping testen
ping YOUR_VPS_IP

# SSH-Verbindung testen
ssh -v root@YOUR_VPS_IP

# Firewall checken (auf Server)
sudo ufw status
```

### Domain zeigt nichts

```bash
# DNS-Propagation checken
nslookup digitalalchemisten.de

# Nginx-Status (auf Server)
sudo systemctl status nginx

# Ghost-Status (auf Server)
cd /var/www/ghost
ghost status
```

---

## 🧙‍♂️ Support

Bei Fragen oder Problemen:

1. **Dokumentation**: Siehe `VPS_ANLEITUNG.md` oder `CLAUDE.md`
2. **Ghost Docs**: https://ghost.org/docs/
3. **Ghost Forum**: https://forum.ghost.org/
4. **GitHub Issues**: https://github.com/enving/ghost_blogging/issues

---

**Viel Erfolg mit Digitalalchemisten!** 🚀✨
