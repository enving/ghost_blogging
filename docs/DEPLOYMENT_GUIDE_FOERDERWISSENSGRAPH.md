# 🚀 Deployment Guidelines für foerderwissensgraph.digitalalchemisten.de

## Übersicht

Diese Subdomain wird auf dem gleichen VPS wie `digitalalchemisten.de` (Ghost Blog) gehostet.  
**VPS IP**: 217.154.164.31  
**Host-Nginx**: Verwaltet alle eingehenden Requests und routet an die entsprechenden Services.

---

## ⚠️ WICHTIGE REGELN

### 1. Keine eigenständigen Port-Änderungen!
Der Host-Nginx erwartet:
- **Port 8080**: HTTP (für interne Kommunikation)
- **Port 8443**: HTTPS (aktuell in Verwendung)

**Wenn du Ports änderst, MUSS der Host-Nginx angepasst werden!**

### 2. SSL/HTTPS Handling
Der **Host-Nginx** übernimmt das SSL-Termination vom Internet:
```
Internet → Host-Nginx (443) → Container (8443)
```

**NICHT zusätzlich HTTP→HTTPS Redirects im Container machen!**  
Das führt zu Redirect-Loops.

### 3. Container-Konfiguration
Dein Container sollte:
- ✅ Auf Port 8443 (HTTPS) lauschen
- ✅ `X-Forwarded-Proto` Header respektieren
- ❌ **KEINE** eigenen HTTP→HTTPS Redirects machen
- ❌ **KEINE** Domains/Hostnames hardcoden

---

## 📁 Aktuelle Host-Nginx Konfiguration

```nginx
# /etc/nginx/sites-available/foerderwissensgraph.conf

server {
    listen 80;
    server_name foerderwissensgraph.digitalalchemisten.de;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name foerderwissensgraph.digitalalchemisten.de;

    ssl_certificate /etc/letsencrypt/live/digitalalchemisten.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/digitalalchemisten.de/privkey.pem;

    location / {
        proxy_pass https://127.0.0.1:8443;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_ssl_verify off;
        
        # Timeouts für LLM-Responses
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
```

---

## 🔧 Änderungen an der Infrastruktur

**Vor jeder Änderung:**
1. Informiere den VPS-Admin (Tristan/enving)
2. Teste lokal mit `docker-compose up`
3. Dokumentiere welche Ports du verwendest

**Bei Problemen:**
- Ghost Blog Repository: `enving/ghost_blogging`
- Dort liegen die Nginx-Scripts für den Host

---

## 📋 Checkliste vor Deployment

- [ ] Container startet auf Port 8443 (HTTPS)
- [ ] Keine doppelten HTTPS-Redirects
- [ ] `docker ps` zeigt korrekte Port-Mappings
- [ ] Kein Hardcoding von Domains im Container
- [ ] Secrets sind in `.env`, nicht im Code

---

## 🚨 Bei Problemen

1. **Redirect-Loop?** → Container macht eigene HTTPS-Redirects
2. **502 Bad Gateway?** → Container läuft nicht oder falscher Port
3. **SSL-Fehler?** → Let's Encrypt Zertifikat erneuern

**Diagnose-Befehle:**
```bash
# Container-Status
docker ps

# Ports checken
ss -tlpn | grep -E ':(8080|8443)'

# Nginx testen
nginx -t

# Logs
docker logs <container_name>
journalctl -u nginx -f
```

---

## 📞 Kontakt

**VPS-Admin**: Tristan (@enving)  
**Repository**: github.com/enving/ghost_blogging

Bei Fragen oder Änderungen bitte vorher absprechen! 🙏
