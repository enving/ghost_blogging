# n8n auf dem Ghost-VPS

n8n läuft neben Ghost auf demselben IONOS-VPS.

| Komponente | Wert |
|------------|------|
| **URL** | https://n8n.digitalalchemisten.de |
| **Container** | `n8n` (Docker, Image `docker.n8n.io/n8nio/n8n:stable`) |
| **Lokal** | `127.0.0.1:5678` (nur über nginx erreichbar) |
| **Server-Verzeichnis** | `/opt/n8n` (`docker-compose.yml`, `.env`) |
| **Daten** | Docker-Volume `n8n_n8n_data` (SQLite, Workflows, Credentials) |
| **nginx** | `/etc/nginx/sites-available/n8n`, TLS über certbot |
| **Quelle im Repo** | [`infra/n8n/`](../infra/n8n/) |

## Zugang für Agenten

Es gibt keinen SSH-Schlüssel-Zugang. Alles läuft über GitHub Actions mit den Repo-Secrets:

```bash
# Einrichten / erneut ausführen / nach Änderungen an infra/n8n ausrollen
gh workflow run manage.yml --ref <branch> -f script=setup_n8n.py
gh run watch
```

`setup.sh` ist idempotent. **Die Actions-Logs sind öffentlich** – Skripte dürfen
keine Secrets, `.env`-Inhalte oder Credentials ausgeben.

## Wichtig

- **`N8N_ENCRYPTION_KEY`** steht nur in `/opt/n8n/.env` auf dem Server. Geht er verloren,
  sind alle in n8n gespeicherten Credentials unbrauchbar. Separat sichern (Passwortmanager).
- `WEBHOOK_URL` ist auf die öffentliche URL gesetzt – daraus baut n8n Webhook- und
  OAuth-Callback-URLs (z. B. `https://n8n.digitalalchemisten.de/rest/oauth2-credential/callback`).
- nginx wird erst aktiviert, wenn DNS auf den Server zeigt; TLS folgt im selben Lauf.
- **TLS-Falle:** n8n teilt sich Port 443 mit Ghost und muss dasselbe TLS-Snippet nutzen
  (`/etc/nginx/snippets/ssl-params.conf`). Mit certbots eigenen Optionen scheitern Firefox und
  Safari mit `SSL_ERROR_ILLEGAL_PARAMETER_ALERT` (anderer Cipher nach HelloRetryRequest).
  Deshalb holt certbot nur das Zertifikat (`certonly`), den vHost schreibt `setup.sh`.
  **Nie `certbot --nginx` ohne `certonly` auf diese Domain loslassen.**

## Update

Erneut `setup_n8n.py` über Actions ausführen – zieht das aktuelle `stable`-Image und startet neu.

## Lokale Anbindung (MCP, API, Secrets)

Siehe `~/Documents/Dev/werkzeuge/n8n/AGENTS.md` (MCP-Server für alle Harnesses, Schlüsselbund,
Betrieb, Fallen). Der Encryption Key wurde einmalig RSA-verschlüsselt über die Actions exportiert;
das Skript ist wieder entfernt.
