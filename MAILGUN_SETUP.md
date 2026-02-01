# Mailgun Setup für Digitalalchemisten

## Status: ABGESCHLOSSEN

---

## Zusammenfassung

| Komponente | Wert |
|------------|------|
| **Mailgun Domain** | `mail.digitalalchemisten.de` |
| **Mailgun Region** | EU |
| **Mailgun API URL** | `https://api.eu.mailgun.net` |
| **SMTP Host** | `smtp.eu.mailgun.org` |
| **SMTP Port** | 587 |
| **SMTP User** | `noreply@mail.digitalalchemisten.de` |

### GitHub Secrets (eingerichtet)
- `MAILGUN_API_KEY` - API Key für Newsletter
- `MAILGUN_SMTP_USER_NOREPLY_PASSWORD` - SMTP Passwort für Magic Links

---

## DNS-Einträge bei IONOS (ERLEDIGT)

Diese Einträge wurden am 2026-02-01 gesetzt:

### TXT Record (SPF)
```
Typ:    TXT
Host:   mail
Wert:   v=spf1 include:mailgun.org ~all
```

### TXT Record (DKIM)
```
Typ:    TXT
Host:   email._domainkey.mail
Wert:   k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClh/a4rTqx7V56pNCHH35LRAXMhNjr5q2dGu02kQElWdB384CO2M5JcQhzvHHD15v5dHwMljbdVY3n7lO67QgL/HjytVAAslcvoU16zd2lUvp1MTCKHJagA/4/uKhds6LoT4tjwNeIsalQ2HAO1qSFw6Zftp9O2W0YZJWwMTvJzQIDAQAB
```

### CNAME Record (Tracking)
```
Typ:    CNAME
Host:   email.mail
Wert:   eu.mailgun.org
```

---

## Ghost Konfiguration (ERLEDIGT)

### Ghost Admin (Newsletter-Versand)
In Ghost Admin unter Settings → Email newsletter → Mailgun:
- **Mailgun domain:** `mail.digitalalchemisten.de`
- **Mailgun API key:** (siehe GitHub Secret `MAILGUN_API_KEY`)
- **Mailgun base URL:** `https://api.eu.mailgun.net`

### Server Config (Magic Links / Transactional Emails)
Datei: `/var/www/ghost/config.production.json`

```json
{
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
  }
}
```

---

## Was funktioniert jetzt

| Feature | Status |
|---------|--------|
| Subscribe-Button | ✅ Funktioniert |
| Magic Link Login | ✅ Funktioniert |
| Member-Registrierung | ✅ Funktioniert |
| Newsletter-Versand | ✅ Funktioniert |
| E-Mail-Absender | `noreply@mail.digitalalchemisten.de` |

---

## Kosten

**Mailgun Free Plan:** 100 E-Mails/Tag
- Reicht für ~100 Subscriber
- Upgrade auf Basic ($15/Monat) wenn >100 Subscriber

---

## Troubleshooting

### "Magic Link konnte nicht versendet werden"
1. Ghost-Logs prüfen: `ssh root@VPS_IP "journalctl -u ghost_digitalalchemisten-de -n 50"`
2. SMTP-Credentials in config.production.json prüfen
3. Ghost neustarten: `systemctl restart ghost_digitalalchemisten-de`

### E-Mails landen im Spam
- SPF, DKIM und CNAME Records alle korrekt gesetzt
- Domain-Reputation braucht Zeit (normal bei neuen Domains)

### Newsletter kommt nicht an
- Mailgun API Key in Ghost Admin prüfen
- Mailgun Region muss EU sein (`https://api.eu.mailgun.net`)

---

## Wichtige Links

- **Mailgun Dashboard:** https://app.mailgun.com
- **Ghost Admin:** https://digitalalchemisten.de/ghost
- **Ghost Logs:** `ssh root@VPS_IP "journalctl -u ghost_digitalalchemisten-de -f"`

---

**Abgeschlossen:** 2026-02-01
**Getestet:** Subscribe + Magic Link funktionieren
