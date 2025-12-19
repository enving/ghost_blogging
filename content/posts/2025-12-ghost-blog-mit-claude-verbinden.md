# Ghost Blog mit Claude verbinden: Die komplette Anleitung für Einsteiger

**Schwierigkeitsgrad**: Fortgeschritten (aber machbar!)
**Zeit**: 60-90 Minuten
**Konzepte**: Ghost CMS, VPS, API, Claude Integration

## Mein "Aha!"-Moment mit Ghost und Claude

Vor ein paar Tagen saß ich vor meinem Laptop und dachte: "Wäre es nicht cool, wenn Claude direkt Blogposts auf meinem eigenen Blog veröffentlichen könnte?"

Nicht auf Medium. Nicht auf Substack. Sondern auf **meinem** Blog. Mit **meiner** Domain. Ohne Ads. Ohne Algorithmus. Einfach... souverän.

Spoiler: Es hat funktioniert. Und dieser Post wurde tatsächlich von Claude geschrieben und automatisch veröffentlicht.

Heute zeige ich dir, wie du das auch schaffst.

## Was du am Ende haben wirst

Nach dieser Anleitung hast du:

✅ Deinen eigenen Ghost Blog auf einem VPS (für ~3€/Monat)
✅ SSL-Verschlüsselung (https://)
✅ Claude, der direkt Posts auf deinem Blog erstellen kann
✅ Volle Kontrolle über deine Inhalte
✅ Keine Abhängigkeit von Drittplattformen

**Zeitaufwand**: 1-2 Stunden beim ersten Mal
**Kosten**: Ab 3€/Monat für den Server
**Vorkenntnisse**: Grundlegende Kommandozeilen-Kenntnisse helfen, sind aber nicht zwingend

## Was du brauchst

**Hardware/Software**:
- Einen Computer (Windows, Mac, Linux - egal)
- Eine Domain (optional, geht auch mit IP erstmal)
- SSH-Zugang zu einem Terminal

**Services** (alle Kosten transparent):
- VPS bei IONOS (~3€/Monat) oder Hetzner (~4€/Monat)
- Domain bei Namecheap/Ionos (~12€/Jahr) - optional
- Claude Code (kostenlos für Basis-Nutzung)

**Zeit**:
- VPS-Bereitstellung: 5-10 Minuten
- Ghost Installation: 20-30 Minuten
- Claude Integration: 15-20 Minuten
- Puffer für "wtf passiert hier": 30 Minuten 😅

## Teil 1: Der VPS - Dein eigener Server

### Warum überhaupt ein VPS?

VPS = Virtual Private Server. Im Grunde: Ein Computer in einem Rechenzentrum, der nur dir gehört.

**Vorteile**:
- Du besitzt deine Daten
- Keine Plattform-Regeln
- Keine Algorithmen
- Volle Kontrolle
- Lerneffekt: Du verstehst, wie das Internet wirklich funktioniert

**VPS-Empfehlung für Anfänger**:

Ich nutze **IONOS VPS S**:
- 2 vCPU Cores
- 2 GB RAM
- 80 GB Speicher
- **2€/Monat** für die ersten 24 Monate

Alternative: **Hetzner CX11** (~4€/Monat, auch top)

### VPS bestellen (5 Minuten)

1. Gehe zu ionos.de → VPS
2. Wähle "VPS S" (2€/Monat Angebot)
3. Betriebssystem: **Ubuntu 22.04 LTS**
4. SSH-Key: Erstmal keinen (machen wir später)
5. Bestellen & auf Email warten

Du bekommst:
- Eine IP-Adresse (z.B. 217.154.164.31)
- Root-Passwort per Email
- SSH-Zugang

### Erster SSH-Login (5 Minuten)

**Windows**: PowerShell öffnen
**Mac/Linux**: Terminal öffnen

```bash
ssh root@DEINE-IP-ADRESSE
# Passwort aus der Email eingeben
```

**Wenn du drin bist**: Du siehst sowas wie `root@ubuntu:~#`

🎉 **Glückwunsch! Du bist auf deinem eigenen Server!**

### Server absichern (10 Minuten)

Erster Schritt: Updates installieren

```bash
apt update && apt upgrade -y
```

Das kann 5-10 Minuten dauern. Mach dir einen Kaffee ☕

**Firewall einrichten**:

```bash
# Erlaube SSH, HTTP, HTTPS
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

**Brute-Force-Schutz**:

```bash
apt install -y fail2ban unattended-upgrades
systemctl enable fail2ban
systemctl start fail2ban
```

✅ **Dein Server ist jetzt grundlegend abgesichert!**

## Teil 2: Ghost CMS installieren

### Was ist Ghost?

Ghost ist eine Open-Source Blogging-Plattform. Denk an WordPress, aber:
- Moderner
- Schneller
- Fokus auf Publishing statt "alles können"
- Eingebautes Newsletter-System
- REST API für Automatisierung

### Node.js installieren (notwendig für Ghost)

```bash
# Node.js v22 LTS installieren
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Version checken
node --version  # sollte v22.x.x anzeigen
```

### Ghost CLI installieren

```bash
npm install ghost-cli@latest -g
```

### Ghost-User erstellen (Security Best Practice)

```bash
adduser --disabled-password --gecos "" ghostuser
usermod -aG sudo ghostuser
```

### Ghost installieren (der spannende Teil!)

```bash
# Verzeichnis erstellen
mkdir -p /var/www/ghost
chown ghostuser:ghostuser /var/www/ghost

# Als ghostuser wechseln
sudo -i -u ghostuser
cd /var/www/ghost

# Ghost installieren
ghost install
```

**Jetzt wird's interaktiv!** Ghost fragt dich:

**Frage 1: Enter your blog URL**
- Mit Domain: `https://deinblog.de`
- Ohne Domain (erstmal): `http://DEINE-IP`

**Frage 2: MySQL hostname**
- Einfach **Enter** drücken (localhost)

**Frage 3: MySQL username**
- `root` eingeben

**Frage 4: MySQL password**
- Ein sicheres Passwort (z.B. `MeinBlog2024Secure!`)
- **Aufschreiben!**

**Frage 5: Ghost database name**
- **Enter** (nimmt Default `ghost_prod`)

**Frage 6: Set up Nginx?**
- `Y` (Ja!)

**Frage 7: Set up SSL?**
- Wenn du eine Domain hast: `Y`
- Ohne Domain: `n` (machen wir später)

**Frage 8: Email für SSL**
- Deine Email eingeben

**Frage 9: Set up systemd?**
- `Y` (damit Ghost automatisch startet)

**Frage 10: Start Ghost?**
- `Y` (natürlich!)

### Moment der Wahrheit

Öffne deinen Browser:
- **http://DEINE-IP** (ohne SSL)
- oder **https://deinblog.de** (mit SSL)

**Siehst du die Ghost-Startseite?** 🎉

### Admin-Account erstellen

Gehe zu: `https://deinblog.de/ghost`

1. **Site title**: Dein Blog-Name
2. **Full name**: Dein Name
3. **Email**: Deine Email
4. **Password**: Sicheres Passwort (min. 10 Zeichen)

✅ **Dein Ghost Blog läuft!**

## Teil 3: Claude mit Ghost verbinden

Jetzt wird's richtig cool. Wir verbinden Claude mit deinem Blog, sodass er direkt Posts erstellen kann.

### Ghost API-Key generieren

1. Ghost Admin → **Settings** (⚙️ unten links)
2. **Integrations** → **Add custom integration**
3. Name: `Claude API`
4. **Create**

Du siehst jetzt:
- **Content API Key**: (für Lesen)
- **Admin API Key**: (für Schreiben) ← **das brauchen wir!**

**Admin API Key kopieren!** Format: `{id}:{secret}`

Beispiel: `6944137adf2eb87ea2bd3147:cfce425840a431ab5...`

### .env Datei erstellen (lokal auf deinem PC)

Erstelle in deinem Blog-Projekt eine `.env` Datei:

```bash
# .env
GHOST_API_URL=https://deinblog.de
GHOST_ADMIN_API_KEY=DEIN-ADMIN-API-KEY-HIER
GHOST_API_VERSION=v5.0
```

**Wichtig**: Diese Datei NIE in Git committen!

```bash
# .gitignore
.env
.env.local
.env.production
```

### Ghost API Publisher Skill erstellen

Erstelle diese Datei: `.claude/skills/ghost_api_publisher/SKILL.md`

```markdown
# Ghost API Publisher Skill

## Purpose
Interact with Ghost Admin API to create and publish blog posts.

## Authentication
Uses JWT authentication with credentials from .env file.

## Python Example

```python
import requests
import jwt
import time

# Load from .env
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('GHOST_API_URL='):
            API_URL = line.split('=', 1)[1].strip() + '/ghost/api/admin'
        elif line.startswith('GHOST_ADMIN_API_KEY='):
            API_KEY = line.split('=', 1)[1].strip()

# Split key
key_id, key_secret = API_KEY.split(':')

# Generate JWT (expires in 5 min)
iat = int(time.time())
token = jwt.encode(
    {'iat': iat, 'exp': iat + 300, 'aud': '/admin/'},
    bytes.fromhex(key_secret),
    algorithm='HS256',
    headers={'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
)

# Create post
headers = {
    'Authorization': f'Ghost {token}',
    'Content-Type': 'application/json',
    'Accept-Version': 'v5.0'
}

post_data = {
    "posts": [{
        "title": "Mein erster Claude-Post!",
        "html": "<p>Dieser Post wurde von Claude erstellt!</p>",
        "status": "draft",  # oder "published"
        "tags": ["Test"]
    }]
}

response = requests.post(f"{API_URL}/posts/", json=post_data, headers=headers)
print(response.json())
```
```

### Test: Ersten Post via API erstellen

```bash
# Python venv erstellen
python3 -m venv .venv
.venv/bin/pip install pyjwt requests

# Script ausführen
.venv/bin/python3 test-post.py
```

**Wenn du `Status Code: 201` siehst**: 🎉 **Es funktioniert!**

Gehe zu Ghost Admin → Posts → Du siehst deinen neuen Draft!

## Teil 4: Claude Skills konfigurieren

### Blog-Post-Writer Skill

Erstelle `.claude/skills/blog_post_writer/SKILL.md`:

```markdown
# Blog-Post Writer Skill

## Mission
Schreibe packende, verständliche Blog-Posts im Stil von [dein Blog].

## Tonalität
- Persönlich & authentisch
- Storytelling statt trockene Fakten
- Für Nicht-Techniker verständlich
- Ehrlich über Fehler

## Struktur
1. Hook (Problem oder Story)
2. Versprechen (Was lernt der Leser?)
3. Hauptteil (mit Beispielen)
4. Praktischer Nutzen (Was jetzt tun?)
5. Ehrliches Fazit

## Beispiel-Hook
"Vor drei Tagen wollte ich meinen eigenen Blog starten.
Nach 4 Stunden Frust hatte ich aufgegeben.
Gestern hab ich's nochmal probiert - diesmal mit System.
Jetzt läuft der Blog. Hier ist wie..."
```

### Workflow kombinieren

Jetzt kommt die Magie:

1. **Du sagst zu Claude**: "Schreib einen Post über Docker für Anfänger"
2. **Claude nutzt Blog-Post-Writer Skill**: Erstellt Content im richtigen Stil
3. **Claude nutzt Ghost API Publisher Skill**: Erstellt Draft in Ghost
4. **Du reviewst** im Ghost Admin
5. **Du publishst** (oder Claude macht es via API)

## Was kann schiefgehen? (Troubleshooting)

### Ghost startet nicht

```bash
# Logs checken
journalctl -u ghost_deinblog-de -n 50

# Häufigster Fehler: MySQL läuft nicht
systemctl status mysql
systemctl start mysql
```

### SSL-Fehler

```bash
# Certbot manuell ausführen
apt install -y certbot python3-certbot-nginx
certbot --nginx -d deinblog.de
```

### API-Fehler "401 Unauthorized"

- JWT Token abgelaufen (max 5 min Gültigkeit)
- Admin API Key falsch kopiert
- Base URL falsch (muss `https://` sein wenn SSL aktiv)

### "502 Bad Gateway"

Ghost ist abgestürzt:

```bash
systemctl restart ghost_deinblog-de
```

## Kosten-Transparenz

**Monatlich**:
- VPS: 2-4€
- Domain: ~1€ (12€/Jahr)
- SSL: 0€ (Let's Encrypt)
- Ghost: 0€ (Open Source)
- **Total: ~3-5€/Monat**

**Zum Vergleich**:
- Ghost(Pro): ab 9$/Monat
- Medium: 5$/Monat (aber nicht deine Domain)
- Substack: "Kostenlos" (aber 10% von Paid Subs)

## Ist das den Aufwand wert?

**Ja, wenn**:
- ✅ Du Kontrolle über deine Daten willst
- ✅ Du keine Plattform-Regeln magst
- ✅ Du etwas lernen willst
- ✅ Du einen Newsletter brauchst
- ✅ Du später monetarisieren willst (Paid Memberships)

**Nein, wenn**:
- ❌ Du nur "schnell bloggen" willst
- ❌ Server-Admin dich abschreckt
- ❌ Du mit Medium/Substack zufrieden bist

**Mein Fazit**: Die ersten 2 Stunden sind Arbeit. Danach läuft es. Und das Gefühl, deinen eigenen Stack zu haben? Unbezahlbar.

## Was als nächstes?

**Nach diesem Setup kannst du**:
1. Theme anpassen (Ghost Themes sind Handlebars-Templates)
2. Newsletter einrichten (Mailgun/SendGrid)
3. Members & Paid Subscriptions aktivieren
4. Custom Domain für Ghost Admin
5. Automatische Backups einrichten
6. Analytics (Plausible, Matomo - DSGVO-konform)

## Deine nächsten Schritte

1. **Heute**: VPS bestellen
2. **Morgen**: Ghost installieren & Admin-Account erstellen
3. **Übermorgen**: Claude integrieren & ersten Test-Post
4. **Nächste Woche**: Ersten echten Post veröffentlichen

## Fragen? Probleme?

Schreib mir: [deine-email@domain.com]

Oder kommentier hier - ich helfe gerne! 👇

---

## Ressourcen

**Offizielle Docs**:
- Ghost Docs: https://ghost.org/docs/
- Ghost API: https://ghost.org/docs/admin-api/

**Tools**:
- IONOS VPS: https://www.ionos.de/hosting/vps
- Hetzner Cloud: https://www.hetzner.com/cloud
- Let's Encrypt: https://letsencrypt.org/

**Community**:
- Ghost Forum: https://forum.ghost.org/
- r/ghost: https://reddit.com/r/ghost/

---

**Geschrieben von**: Claude (mit Anleitung von Tristan)
**Erstellt**: 2025-12-18
**Tags**: #Ghost #Self-Hosting #Tutorial #Claude #AI-Integration #Für-Einsteiger
**Geschätzte Lesezeit**: 15 Minuten

---

*P.S.: Ja, dieser Post wurde tatsächlich von Claude geschrieben und automatisch als Draft in Ghost erstellt. Meta, oder? 😄*
