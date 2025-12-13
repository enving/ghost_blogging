# VPS Deployment: Digitalalchemisten

**Server**: YOUR_VPS_IP
**OS**: Ubuntu 22.04
**Domain**: digitalalchemisten.de

---

## Schritt 1: SSH-Verbindung testen

```bash
ssh root@YOUR_VPS_IP
```

Beim ersten Mal:
- Fingerprint bestätigen (yes)
- Root-Passwort eingeben (von IONOS)

---

## Schritt 2: Setup-Script hochladen & ausführen

### Von deinem Rechner:

```bash
# Script auf Server kopieren
scp vps-setup.sh root@YOUR_VPS_IP:/root/

# Auf Server einloggen
ssh root@YOUR_VPS_IP

# Script ausführbar machen
chmod +x /root/vps-setup.sh

# Script ausführen
./vps-setup.sh
```

**Was das Script macht**:
- ✅ System-Updates
- ✅ Firewall (SSH, HTTP, HTTPS)
- ✅ Fail2ban (Brute-Force-Schutz)
- ✅ Node.js LTS
- ✅ Ghost-User erstellen
- ✅ Ghost CLI installieren

**Dauer**: ~5 Minuten

---

## Schritt 3: Ghost installieren (als ghostuser)

```bash
# Zu ghostuser wechseln
sudo -i -u ghostuser

# Ins Ghost-Verzeichnis
cd /var/www/ghost

# Ghost installieren
ghost install
```

### Ghost Setup-Fragen:

```
? Enter your blog URL: https://digitalalchemisten.de
? Enter your MySQL hostname: localhost
? Enter your MySQL username: root
? Enter your MySQL password: [Enter für auto-generiert]
? Enter your Ghost database name: ghost_prod

? Do you wish to set up Nginx? Yes
? Do you wish to set up SSL? Yes
? Enter your email (for SSL certificate): deine@email.de

? Do you wish to set up systemd? Yes
? Do you want to start Ghost? Yes
```

**Wichtig**: Bei SSL braucht Ghost deine Email für Let's Encrypt!

---

## Schritt 4: Domain DNS konfigurieren

### Bei deinem Domain-Anbieter (wo digitalalchemisten.de registriert ist):

**A-Record erstellen**:
```
Type: A
Name: @
Value: YOUR_VPS_IP
TTL: 3600 (oder auto)
```

**Optional - WWW-Weiterleitung**:
```
Type: CNAME
Name: www
Value: digitalalchemisten.de
TTL: 3600
```

**Propagation**: Dauert 5 Minuten bis 24 Stunden (meist ~1 Stunde)

**Testen**:
```bash
# Auf deinem Rechner
ping digitalalchemisten.de

# Sollte YOUR_VPS_IP zeigen
```

---

## Schritt 5: Ghost Admin erstellen

```
1. Öffne: https://digitalalchemisten.de/ghost
2. Erstelle Admin-Account:
   - Name: Tristan (oder wie du willst)
   - Email: deine@email.de
   - Password: [sicher!]
   - Blog Title: Digitalalchemisten (oder ändern)
```

---

## Schritt 6: Lokale Posts importieren

### Option A: Export von lokal → Import auf Server

**Lokal (http://localhost:2368/ghost)**:
```
1. Settings → Labs → Export
2. Lädt eine JSON-Datei runter
```

**Auf Server (https://digitalalchemisten.de/ghost)**:
```
1. Settings → Labs → Import content
2. JSON-File hochladen
3. Fertig!
```

### Option B: Manuell copy & paste

- Öffne deine Markdown-Files in `content/posts/`
- Erstelle neue Posts auf dem Server
- Copy & Paste den Content

---

## Schritt 7: Erste Tests

```
✅ Blog erreichbar?         → https://digitalalchemisten.de
✅ Admin erreichbar?        → https://digitalalchemisten.de/ghost
✅ SSL funktioniert?        → Schloss-Symbol im Browser
✅ Posts sichtbar?          → Mindestens einer published
✅ Responsive?              → Auf Handy testen
```

---

## Troubleshooting

### Problem: "ghost install" hängt bei MySQL

**Lösung**:
```bash
# MySQL manuell installieren
sudo apt install mysql-server -y

# Dann ghost install nochmal
ghost install
```

### Problem: Domain zeigt nichts

**Check DNS**:
```bash
nslookup digitalalchemisten.de
# Sollte YOUR_VPS_IP zeigen
```

**Check Nginx**:
```bash
sudo systemctl status nginx
# Sollte "active (running)" zeigen
```

### Problem: SSL-Zertifikat fehlgeschlagen

**Ursachen**:
- Domain zeigt noch nicht auf Server (DNS)
- Port 80/443 nicht offen (Firewall check)

**Lösung**:
```bash
# SSL manuell nachholen
cd /var/www/ghost
ghost setup ssl
```

### Problem: Ghost startet nicht

**Logs checken**:
```bash
cd /var/www/ghost
ghost log

# Oder systemd logs
sudo journalctl -u ghost_digitalalchemisten-de -n 50
```

---

## Nützliche Ghost-Befehle

```bash
# Status checken
ghost status

# Ghost neustarten
ghost restart

# Ghost stoppen
ghost stop

# Ghost starten
ghost start

# Updates installieren
ghost update

# Logs anzeigen
ghost log
```

---

## Backup-Strategie

### Automatisches Backup (täglich)

**Script erstellen**: `/home/ghostuser/backup-ghost.sh`

```bash
#!/bin/bash
# Backup Ghost Content & Database

BACKUP_DIR="/home/ghostuser/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup erstellen
cd /var/www/ghost
ghost backup --filename "$BACKUP_DIR/ghost_$DATE.zip"

# Alte Backups löschen (älter als 7 Tage)
find $BACKUP_DIR -name "ghost_*.zip" -mtime +7 -delete

echo "✅ Backup erstellt: ghost_$DATE.zip"
```

**Cron-Job einrichten**:
```bash
crontab -e

# Täglich um 3 Uhr morgens
0 3 * * * /home/ghostuser/backup-ghost.sh
```

---

## Performance-Optimierung (später)

### 1. Nginx-Caching
```nginx
# /etc/nginx/sites-available/digitalalchemisten.de

location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 2. Image-Optimierung
```bash
# WebP-Support
apt install webp

# Images konvertieren
find /var/www/ghost/content/images -name "*.jpg" -exec cwebp {} -o {}.webp \;
```

### 3. CDN (optional)
- Cloudflare (gratis)
- BunnyCDN (günstig)

---

## Security-Checklist

- [x] Firewall aktiv (UFW)
- [x] Fail2ban läuft
- [x] SSL-Zertifikat (A+ Rating?)
- [x] SSH-Key statt Password (optional, aber empfohlen)
- [x] Automatische Updates aktiviert
- [x] Regelmäßige Backups (täglich)
- [ ] Ghost auf latest Version
- [ ] Monitoring (Uptime Robot)

**SSL-Rating testen**:
https://www.ssllabs.com/ssltest/analyze.html?d=digitalalchemisten.de

---

## Monitoring & Alerts

### Uptime Robot (kostenlos)

1. Account erstellen: https://uptimerobot.com
2. Monitor hinzufügen:
   - Type: HTTPS
   - URL: https://digitalalchemisten.de
   - Interval: 5 Minuten
3. Alert-Kontakte: Deine Email

**Benachrichtigung wenn**:
- Site down
- SSL-Zertifikat läuft ab (30 Tage vorher)

---

## Kosten-Übersicht

| Posten | Kosten |
|--------|--------|
| VPS S (IONOS) | 2€/Monat |
| Domain (bereits vorhanden) | ~1€/Monat |
| SSL (Let's Encrypt) | 0€ |
| **Total** | **3€/Monat** |

Günstiger als ein Netflix-Abo! 🎉

---

## Nächste Schritte nach Go-Live

1. **Content erstellen**:
   - 5-10 Posts für Start
   - "Über mich" Seite
   - Impressum & Datenschutz (DSGVO!)

2. **Theme customizen**:
   - Farben anpassen
   - Logo hochladen
   - Navigation strukturieren

3. **Newsletter einrichten**:
   - Mailgun-Account (gratis bis 5k Emails)
   - Ghost Newsletter aktivieren

4. **Analytics**:
   - Plausible (DSGVO-konform) oder
   - Ghost built-in Analytics

5. **Social Media**:
   - Twitter/X Account
   - GitHub für Tech-Content
   - LinkedIn?

---

**Bei Problemen**: Sag Bescheid, ich helfe! 🧙‍♂️
