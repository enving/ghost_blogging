#!/bin/bash
# Digitalalchemisten VPS Setup Script
# Server: YOUR_VPS_IP
# OS: Ubuntu 22.04

set -e  # Exit on error

echo "🧙‍♂️ Digitalalchemisten VPS Setup startet..."
echo "============================================"

# 1. System Update
echo "📦 System wird aktualisiert..."
apt update && apt upgrade -y

# 2. Firewall Setup
echo "🔥 Firewall wird konfiguriert..."
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

# 3. Security Tools
echo "🛡️ Security-Tools werden installiert..."
apt install -y fail2ban unattended-upgrades

# Fail2ban konfigurieren
systemctl enable fail2ban
systemctl start fail2ban

# 4. Node.js installieren (LTS)
echo "📦 Node.js wird installiert..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs

echo "✅ Node.js Version:"
node --version
npm --version

# 5. Ghost User erstellen
echo "👤 Ghost-User wird erstellt..."
if ! id "ghostuser" &>/dev/null; then
    adduser --disabled-password --gecos "" ghostuser
    usermod -aG sudo ghostuser
    echo "✅ User 'ghostuser' erstellt"
else
    echo "ℹ️ User 'ghostuser' existiert bereits"
fi

# 6. Ghost CLI installieren
echo "👻 Ghost CLI wird installiert..."
npm install ghost-cli@latest -g

# 7. Ghost-Verzeichnis vorbereiten
echo "📁 Ghost-Verzeichnis wird vorbereitet..."
mkdir -p /var/www/ghost
chown ghostuser:ghostuser /var/www/ghost
chmod 775 /var/www/ghost

echo ""
echo "✅ Basis-Setup abgeschlossen!"
echo ""
echo "🎯 Nächste Schritte (als ghostuser):"
echo "   sudo -i -u ghostuser"
echo "   cd /var/www/ghost"
echo "   ghost install"
echo ""
echo "📝 Während Ghost Install:"
echo "   - Blog URL: https://digitalalchemisten.de"
echo "   - MySQL: Ja"
echo "   - Nginx: Ja"
echo "   - SSL: Ja (Let's Encrypt)"
echo "   - Systemd: Ja"
echo ""
echo "🧙‍♂️ Viel Erfolg!"
