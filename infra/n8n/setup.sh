#!/usr/bin/env bash
# n8n auf dem Ghost-VPS einrichten. Als root auf dem Server ausführen:
#   bash setup.sh n8n.digitalalchemisten.de
# Idempotent: mehrfach ausführbar, überschreibt keinen bestehenden Encryption Key.
# Gibt keine Secrets aus.
set -euo pipefail

DOMAIN="${1:-n8n.digitalalchemisten.de}"
DIR=/opt/n8n
SRC="$(cd "$(dirname "$0")" && pwd)"
SITE=/etc/nginx/sites-available/n8n

echo "== Ressourcen"
free -h
df -h / | tail -1

# Der VPS hat nur ~1,8 GB RAM (Ghost + MySQL belegen ~1 GB). Swap als Puffer,
# damit der OOM-Killer bei Lastspitzen nicht Ghost oder MySQL trifft.
if [ "$(swapon --show --noheadings | wc -l)" -eq 0 ]; then
  echo "   kein Swap vorhanden – lege /swapfile (2 GB) an"
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile >/dev/null
  swapon /swapfile
  grep -q '^/swapfile ' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
  sysctl -q vm.swappiness=10
  echo 'vm.swappiness=10' > /etc/sysctl.d/99-swappiness.conf
fi

AVAIL_MB=$(free -m | awk '/^Mem:/{m=$7} /^Swap:/{s=$4} END{print m+s}')
if [ "$AVAIL_MB" -lt 1200 ]; then
  echo "!! Nur ${AVAIL_MB} MB RAM+Swap frei – zu wenig für n8n. Abbruch (FORCE=1 zum Übergehen)."
  [ "${FORCE:-0}" = "1" ] || exit 1
fi

echo "== Docker"
if ! command -v docker >/dev/null; then
  apt-get update -qq
  apt-get install -y -qq ca-certificates curl
  curl -fsSL https://get.docker.com | sh
fi
docker compose version >/dev/null

echo "== Dateien nach $DIR"
mkdir -p "$DIR"
install -m 644 "$SRC/docker-compose.yml" "$DIR/docker-compose.yml"
if [ ! -f "$DIR/.env" ]; then
  umask 077
  {
    echo "N8N_DOMAIN=$DOMAIN"
    echo "N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)"
  } > "$DIR/.env"
  echo "   .env neu erzeugt (Encryption Key NICHT verlieren – liegt in $DIR/.env)"
else
  sed -i "s/^N8N_DOMAIN=.*/N8N_DOMAIN=$DOMAIN/" "$DIR/.env"
  echo "   .env vorhanden, Key bleibt"
fi
chmod 600 "$DIR/.env"

echo "== n8n starten"
cd "$DIR"
docker compose pull -q
docker compose up -d
for i in $(seq 1 30); do
  curl -fsS -o /dev/null http://127.0.0.1:5678/healthz && { echo "   n8n antwortet"; break; }
  sleep 2
  [ "$i" = 30 ] && { echo "!! n8n antwortet nicht"; docker compose logs --tail 30; exit 1; }
done

# nginx erst aktivieren, wenn DNS stimmt – dann folgt TLS im selben Lauf.
# Vorher ist n8n nur auf 127.0.0.1 erreichbar (keine offene Owner-Einrichtung per HTTP).
echo "== DNS"
SERVER_IP=$(curl -fsS -4 https://ifconfig.me || true)
DNS_IP=$(getent ahostsv4 "$DOMAIN" | awk 'NR==1{print $1}' || true)
if [ -z "$DNS_IP" ] || [ "$DNS_IP" != "$SERVER_IP" ]; then
  echo "!! DNS für $DOMAIN zeigt auf '${DNS_IP:-nichts}', Server ist $SERVER_IP."
  echo "   n8n läuft lokal. Nach dem DNS-Eintrag setup.sh erneut ausführen."
  exit 0
fi

# TLS-Einstellungen von Ghost übernehmen (gemeinsamer Port 443, siehe nginx-n8n.conf).
SSL_SNIPPET=/etc/nginx/snippets/ssl-params.conf
[ -f "$SSL_SNIPPET" ] || SSL_SNIPPET=/etc/letsencrypt/options-ssl-nginx.conf
echo "== nginx (TLS-Snippet: $SSL_SNIPPET)"
nginx -T 2>/dev/null | awk -v s="$SSL_SNIPPET" '/^# configuration file/{f=$4} index($0, "include " s){print "   genutzt von " f}' | sort -u

activate_site() {
  # $1 = Inhalt. Bei fehlerhafter Konfig alte Version wiederherstellen, damit der
  # nächste nginx-Reload (auch Ghosts Zertifikatserneuerung) nicht scheitert.
  [ -f "$SITE" ] && cp "$SITE" "$SITE.bak"
  printf '%s\n' "$1" > "$SITE"
  ln -sf "$SITE" /etc/nginx/sites-enabled/n8n
  if ! nginx -t; then
    if [ -f "$SITE.bak" ]; then mv "$SITE.bak" "$SITE"; else rm -f /etc/nginx/sites-enabled/n8n; fi
    nginx -t || rm -f /etc/nginx/sites-enabled/n8n
    echo "!! nginx-Konfiguration fehlerhaft, vorherigen Stand wiederhergestellt"
    exit 1
  fi
  systemctl reload nginx
}

CERT=/etc/letsencrypt/live/$DOMAIN/fullchain.pem
command -v certbot >/dev/null || apt-get install -y -qq certbot python3-certbot-nginx
if [ ! -f "$CERT" ]; then
  echo "== TLS: Zertifikat holen"
  activate_site "server { listen 80; listen [::]:80; server_name $DOMAIN; location / { return 404; } }"
  certbot certonly --nginx -d "$DOMAIN" --non-interactive --agree-tos \
    --register-unsafely-without-email --deploy-hook "systemctl reload nginx"
fi

echo "== nginx: vHost schreiben"
activate_site "$(sed -e "s|DOMAIN_PLACEHOLDER|$DOMAIN|g" -e "s|SSL_SNIPPET_PLACEHOLDER|$SSL_SNIPPET|" "$SRC/nginx-n8n.conf")"
rm -f "$SITE.bak"

curl -fsS -o /dev/null "https://$DOMAIN/healthz" && echo "   https://$DOMAIN erreichbar"
echo "   Fertig – jetzt sofort das Owner-Konto anlegen!"
