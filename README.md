# Digitalalchemisten - Technologie verständlich gemacht

Ein praxisorientierter Tech-Blog, der komplexe Themen rund um KI, digitale Souveränität und Innovation für Non-Techies zugänglich macht.

**Live:** https://digitalalchemisten.de

---

## 🎯 Mission

Erfahrungen mit digitalen Tools und KI teilen, sodass auch nicht-technische Menschen die spannenden Entwicklungen nachvollziehen und selbst ausprobieren können.

---

## 🚀 Status

| Feature | Status |
|---------|--------|
| Blog online | ✅ |
| Ghost CMS | ✅ |
| SSL/HTTPS | ✅ |
| Subscribe/Newsletter | ✅ |
| Mailgun Integration | ✅ |

---

## 📚 Dokumentation

| Datei | Beschreibung |
|-------|--------------|
| [AGENT_HANDOVER.md](AGENT_HANDOVER.md) | **Für Agents:** Alle technischen Details, Secrets-Referenz, SSH-Zugang |
| [CLAUDE.md](CLAUDE.md) | Vollständiger Projektplan & Vision |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Setup-Anleitung für lokale Entwicklung |
| [VPS_ANLEITUNG.md](VPS_ANLEITUNG.md) | VPS-Deployment Schritt-für-Schritt |
| [MAILGUN_SETUP.md](MAILGUN_SETUP.md) | E-Mail/Newsletter Konfiguration |

---

## 🔧 Technologie-Stack

- **CMS:** Ghost (selbstgehostet)
- **Server:** IONOS VPS (Ubuntu)
- **E-Mail:** Mailgun (EU-Region)
- **SSL:** Let's Encrypt
- **CI/CD:** GitHub Actions

---

## 📂 Repository-Struktur

```
ghost_blogging/
├── content/
│   ├── posts/           # Markdown Blog-Posts
│   ├── glossar/         # Glossar-Einträge
│   └── post_ideas/      # Post-Ideen
├── .github/
│   └── workflows/       # CI/CD Pipelines
├── ghost_docs/          # Ghost API Dokumentation
├── theme-assets/        # Theme-Erweiterungen
├── AGENT_HANDOVER.md    # Agent-Dokumentation
├── CLAUDE.md            # Projektplan
└── README.md            # Diese Datei
```

---

## 🔐 Secrets

Alle sensiblen Daten sind in **GitHub Actions Secrets** gespeichert (nicht im Code!).

Siehe [AGENT_HANDOVER.md](AGENT_HANDOVER.md) für die vollständige Liste.

---

## 📝 Content-Kategorien

- 🤖 KI & Automation
- 🇪🇺 Digitale Souveränität
- 🔧 Self-Hosting Tutorials
- 💡 Innovation & Tools
- 🛡️ Privacy & Security

---

## 💰 Kosten

| Service | Kosten |
|---------|--------|
| IONOS VPS S | 2€/Monat |
| Domain | ~1€/Monat |
| Mailgun | 0€ (Free: 100 E-Mails/Tag) |
| SSL | 0€ (Let's Encrypt) |
| **Total** | **~3€/Monat** |

---

**Letzte Aktualisierung:** 2026-02-01
