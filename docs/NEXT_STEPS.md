# Nächste Schritte: Digitalalchemisten

## ✅ Was bereits fertig ist:

- **Ghost läuft lokal**: http://localhost:2368
- **Admin registriert**: "Digitalalchemisten"
- **GitHub Repository**: Initialisiert mit Struktur
- **2 fertige Blog-Posts**: Bereit zum Importieren
- **Domain vorhanden**: digitalalchemisten.de

---

## 🎯 Sofort-Aktionen (heute/diese Woche):

### 1. Posts in Ghost importieren (5 Min)

**Option A: Copy & Paste** (schnellste Methode)
```
1. Öffne: http://localhost:2368/ghost
2. Klicke: "New Post"
3. Kopiere Content aus: content/posts/2025-01-ghost-blog-setup.md
4. Füge ein im Ghost Editor
5. Veröffentlichen oder als Draft speichern
6. Wiederholen für 2. Post
```

**Option B: Import-Funktion**
```
1. Ghost Admin → Settings → Labs → Import content
2. Markdown-Dateien auswählen
3. Importieren
```

### 2. VPS bei IONOS bestellen

**Was bestellen**:
- **VPS S** (2€/Monat für 24 Monate)
  - 2 vCores CPU
  - 2 GB RAM
  - 80 GB NVMe

**Domain-Einstellung**:
- digitalalchemisten.de → auf VPS zeigen lassen
- DNS A-Record auf VPS-IP

**Link**: https://www.ionos.de/hosting/vps

### 3. GitHub Repository auf GitHub pushen (optional)

```bash
# Auf GitHub: Neues Repository erstellen
# Name: digitalalchemisten

# Dann lokal:
git remote add origin https://github.com/deinusername/digitalalchemisten.git
git branch -M main
git push -u origin main
```

---

## 📋 Nächste Woche (sobald VPS bereit):

### Phase 1: VPS Setup

1. **SSH-Zugang testen**
   ```bash
   ssh root@deine-vps-ip
   ```

2. **Server absichern**
   - Firewall konfigurieren
   - Fail2ban installieren
   - Non-root User erstellen

3. **Ghost Production installieren**
   - Node.js installieren
   - Ghost CLI nutzen
   - SSL via Let's Encrypt

4. **Domain verbinden**
   - DNS A-Record: digitalalchemisten.de → VPS-IP
   - SSL-Zertifikat automatisch

5. **Ersten Deployment**
   - Posts von lokal exportieren
   - Auf Production importieren
   - Live-Test!

---

## 🎨 Content-Ideen für die nächsten Posts:

Basierend auf deinen Erfahrungen:

1. **"Docker für Nicht-Techniker: Container einfach erklärt"**
   - Was wir gerade gemacht haben!
   - Ghost via Docker = perfektes Beispiel

2. **"IONOS VPS Setup: Von Null auf HTTPS in 30 Minuten"**
   - Dokumentiere das VPS-Setup als Tutorial
   - Für andere zum Nachbauen

3. **"Claude Code: Mein KI-Assistent für alles"**
   - Wie du mit mir arbeitest
   - Praktische Beispiele

4. **"Digitale Souveränität: Warum ich nicht auf Medium blogge"**
   - Deine Vision
   - EU vs US Hosting

5. **"GitHub für Blogger: Versionskontrolle für Texte"**
   - Git als Backup-Tool
   - Nicht nur für Programmierer

---

## 🧪 Experimente für später:

- **Newsletter-System**: Mailgun einrichten
- **Custom Theme**: Eigenes Design
- **Analytics**: Plausible (DSGVO-konform)
- **Kommentare**: Utterances via GitHub
- **Search**: Eigene Suchfunktion

---

## 💡 Branding-Ideen: Digitalalchemisten

**Farbschema-Vorschläge**:
- 🟣 **Alchemie-Lila**: Mystisch, aber modern
- 🔵 **Tech-Blau**: Vertrauen, Technologie
- 🟢 **Growth-Grün**: Wachstum, Lernen
- ⚫ **Dark Mode**: Dunkel mit Akzent-Farben

**Logo-Konzepte**:
- Alchemie-Symbol + Binärcode
- Reagenzglas mit digitalen Elementen
- Retorte mit Bits & Bytes

**Slogan-Ideen**:
- "Technologie verständlich gemacht"
- "Wo Bits zu Wissen werden"
- "Digital verstehen, souverän handeln"
- "Von Tech-Alchemy für Techie-Neulinge"

---

## 📊 Projektstatus

**Phase 0: Lokales Setup** ✅ (COMPLETE)
- Ghost lokal läuft
- Repository erstellt
- Erste Posts geschrieben

**Phase 1: VPS Deployment** 🔄 (NEXT)
- VPS bestellen
- Server einrichten
- Domain verbinden
- Go Live!

**Phase 2: Content-Produktion** ⏳ (GEPLANT)
- 10+ Posts schreiben
- Theme customizen
- Newsletter vorbereiten

---

## 🤝 Zusammenarbeit: Wie wir weitermachen

**Dein Token-sparender Workflow**:

1. **Content-Erstellung**:
   ```
   Du: "Schreib einen Post über [Thema]"
   Ich: Erstelle Markdown-File in content/posts/
   Du: Reviewst & importierst in Ghost
   ```

2. **Git-Management**:
   ```
   Ich: Erstelle Commits mit allen Änderungen
   Du: Pushst zu GitHub wenn alles passt
   ```

3. **MCP nur bei Bedarf**:
   ```
   Für normale Posts: KEIN MCP (spart Tokens!)
   Für Automation: MCP aktivieren (später)
   ```

---

**Nächster Chat**: Sag mir sobald VPS bereit ist, dann machen wir Phase 1! 🚀
