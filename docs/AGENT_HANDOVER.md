# Agent Handover - Digitalalchemisten

Dieses Dokument enthält alle Informationen, die ein neuer Agent braucht, um die Arbeit an diesem Projekt fortzusetzen.

**Wichtig:** Dies ist ein öffentliches Repository! Alle Secrets sind in GitHub Actions Secrets gespeichert.

---

## Übersicht

| Komponente | Wert |
|------------|------|
| **Blog URL** | https://digitalalchemisten.de |
| **Ghost Admin** | https://digitalalchemisten.de/ghost |
| **VPS Provider** | IONOS |
| **E-Mail Provider** | Mailgun (EU-Region) |
| **Repository** | https://github.com/enving/ghost_blogging |

---

## GitHub Actions Secrets

Alle sensiblen Daten sind als GitHub Secrets gespeichert:

| Secret | Beschreibung |
|--------|--------------|
| `VPS_IP` | IP-Adresse des IONOS VPS |
| `VPS_USER` | SSH-Benutzername (root) |
| `VPS_PW` | SSH-Passwort |
| `BLOG_URL` | https://digitalalchemisten.de |
| `BLOG_DOMAIN` | digitalalchemisten.de |
| `GHOST_API_URL` | Ghost API URL |
| `GHOST_ADMIN_API_KEY` | Ghost Admin API Key |
| `GHOST_CONTENT_API_KEY` | Ghost Content API Key |
| `GHOST_SUDO_USER_PW` | Ghost Admin User Passwort |
| `MYSQL_HOSTNAME` | localhost |
| `MYSQL_DATABASE_NAME` | ghost_prod |
| `MYSQL_USERNAME` | root |
| `MYSQL_PASSWORD` | MySQL Passwort |
| `MAILGUN_API_KEY` | Mailgun API Key für Newsletter |
| `MAILGUN_URL_SANDBOX` | Sandbox URL (nicht mehr verwendet) |
| `MAILGUN_SMTP_USER_NOREPLY_PASSWORD` | SMTP Passwort für Magic Links |
| `ADMIN_EMAIL` | Admin E-Mail-Adresse |
| `NAME` | Admin Name |
| `PASSWORD` | Allgemeines Passwort |

---

## SSH-Zugang zum VPS

Der SSH-Zugang funktioniert über das `VPS_PW` Secret:

```bash
# Verbindung zum Server (Passwort aus GitHub Secret VPS_PW)
ssh root@$(gh secret get VPS_IP)

# Die IP ist im GitHub Secret VPS_IP gespeichert
```

### Wichtige Pfade auf dem Server

| Pfad | Beschreibung |
|------|--------------|
| `/var/www/ghost/` | Ghost Installation |
| `/var/www/ghost/config.production.json` | Ghost Konfiguration |
| `/var/www/ghost/content/` | Ghost Content (Themes, Images, etc.) |

### Ghost-Befehle auf dem Server

```bash
# Als ghostuser arbeiten
sudo -i -u ghostuser
cd /var/www/ghost

# Ghost Status
ghost status

# Ghost Neustarten
ghost restart

# Ghost Logs
ghost log

# Oder via systemctl
systemctl status ghost_digitalalchemisten-de
systemctl restart ghost_digitalalchemisten-de
journalctl -u ghost_digitalalchemisten-de -f
```

---

## Ghost Konfiguration

Die aktuelle `/var/www/ghost/config.production.json`:

```json
{
  "url": "https://digitalalchemisten.de",
  "server": {
    "port": 2368,
    "host": "127.0.0.1"
  },
  "database": {
    "client": "mysql",
    "connection": {
      "host": "127.0.0.1",
      "user": "root",
      "password": "SIEHE_GITHUB_SECRET_MYSQL_PASSWORD",
      "database": "ghost_prod"
    }
  },
  "mail": {
    "transport": "SMTP",
    "from": "'Digitalalchemisten' <noreply@mail.digitalalchemisten.de>",
    "options": {
      "host": "smtp.eu.mailgun.org",
      "port": 587,
      "secure": false,
      "auth": {
        "user": "noreply@mail.digitalalchemisten.de",
        "pass": "SIEHE_GITHUB_SECRET_MAILGUN_SMTP_USER_NOREPLY_PASSWORD"
      }
    }
  },
  "logging": {
    "transports": ["file", "stdout"]
  },
  "process": "systemd",
  "security": {
    "staffDeviceVerification": false
  },
  "paths": {
    "contentPath": "/var/www/ghost/content"
  }
}
```

---

## Mailgun Setup

| Einstellung | Wert |
|-------------|------|
| Domain | `mail.digitalalchemisten.de` |
| Region | EU |
| API URL | `https://api.eu.mailgun.net` |
| SMTP Host | `smtp.eu.mailgun.org` |
| SMTP Port | 587 |
| SMTP User | `noreply@mail.digitalalchemisten.de` |

### DNS-Einträge bei IONOS (bereits konfiguriert)

| Typ | Host | Wert |
|-----|------|------|
| TXT | `mail` | `v=spf1 include:mailgun.org ~all` |
| TXT | `email._domainkey.mail` | `k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...` |
| CNAME | `email.mail` | `eu.mailgun.org` |

### Ghost Admin Mailgun-Einstellungen

In Ghost Admin → Settings → Email newsletter → Mailgun:
- **Mailgun domain:** `mail.digitalalchemisten.de`
- **Mailgun API key:** (GitHub Secret `MAILGUN_API_KEY`)
- **Mailgun base URL:** `https://api.eu.mailgun.net`

---

## Wichtige Dokumentationen

| Datei | Beschreibung |
|-------|--------------|
| `CLAUDE.md` | Vollständiger Projektplan & Vision |
| `SETUP_GUIDE.md` | Setup-Anleitung für neuen Rechner |
| `VPS_ANLEITUNG.md` | VPS-Deployment Schritt-für-Schritt |
| `MAILGUN_SETUP.md` | E-Mail/Newsletter Konfiguration |
| `NEXT_STEPS.md` | Aktuelle TODOs |

---

## Content-Workflow

### Posts schreiben
1. Markdown-Dateien in `/content/posts/` erstellen
2. Frontmatter mit Metadaten hinzufügen
3. Via Ghost Admin API oder UI veröffentlichen

### Mit Ghost API publizieren
```bash
# Python-Umgebung aktivieren
source ghost_publisher_env/bin/activate

# Post veröffentlichen
python publish_all_posts.py
```

---

## Aktuelle Funktionen

| Feature | Status |
|---------|--------|
| Blog online | ✅ |
| SSL-Zertifikat | ✅ |
| Ghost Admin | ✅ |
| Subscribe-Button | ✅ |
| Magic Link Login | ✅ |
| Newsletter-Versand | ✅ |
| Mailgun Integration | ✅ |

---

## Bekannte Einschränkungen

- **Mailgun Free Plan:** 100 E-Mails/Tag (reicht für ~100 Subscriber)
- **VPS:** IONOS VPS S (2 vCores, 2GB RAM)

---

## Kontakt / Hilfe

- **Ghost Docs:** https://ghost.org/docs/
- **Mailgun Docs:** https://documentation.mailgun.com/
- **Ghost Forum:** https://forum.ghost.org/

---

**Letzte Aktualisierung:** 2026-02-01
**Erstellt von:** Claude Agent Session
