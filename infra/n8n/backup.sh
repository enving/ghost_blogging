#!/usr/bin/env bash
# n8n-Backup auf dem VPS. Liegt als /opt/n8n/backup.sh, läuft per /etc/cron.d/n8n-backup.
#   täglich:  Export von Workflows + Credentials (Credentials bleiben verschlüsselt), ohne Ausfall
#   sonntags: zusätzlich Volume-Abzug; n8n wird dafür ~15 s gestoppt (konsistente SQLite-DB)
#   backup.sh full → Volume-Abzug sofort
# Enthält /opt/n8n/.env (Encryption Key) – nötig, um Credentials wiederherzustellen. Nur root lesbar.
# Wiederherstellen: siehe ~/Documents/Dev/werkzeuge/n8n/AGENTS.md
set -euo pipefail

B=/root/backup/n8n
D=$(date +%F)
mkdir -p "$B"
chmod 700 /root/backup "$B"
umask 077

echo "$(date '+%F %T') Backup-Start"

# 1. Export über die n8n-CLI im laufenden Container
docker exec -u node n8n sh -c 'rm -rf /tmp/bk && mkdir -p /tmp/bk/workflows /tmp/bk/credentials'
docker exec -u node n8n n8n export:workflow --backup --output=/tmp/bk/workflows/ >/dev/null 2>&1 \
  || echo "   Hinweis: keine Workflows exportiert (leer?)"
docker exec -u node n8n n8n export:credentials --backup --output=/tmp/bk/credentials/ >/dev/null 2>&1 \
  || echo "   Hinweis: keine Credentials exportiert (leer?)"
T=$(mktemp -d)
docker cp n8n:/tmp/bk "$T/bk" >/dev/null
docker exec -u node n8n rm -rf /tmp/bk
cp /opt/n8n/.env /opt/n8n/docker-compose.yml "$T/bk/"
tar czf "$B/n8n-export-$D.tgz" -C "$T/bk" .
rm -rf "$T"
echo "   Export: $(find "$B/n8n-export-$D.tgz" -printf '%s') Bytes, $(ls "$B"/n8n-export-*.tgz | wc -l) Stände"

# 2. Volume-Abzug (sonntags oder auf Zuruf)
if [ "$(date +%u)" = 7 ] || [ "${1:-}" = full ]; then
  cd /opt/n8n
  docker compose stop -t 30 n8n >/dev/null 2>&1
  docker run --rm -v n8n_n8n_data:/d:ro -v "$B":/b alpine tar czf "/b/n8n-volume-$D.tgz" -C /d . \
    || echo "!! Volume-Abzug fehlgeschlagen"
  docker compose start n8n >/dev/null 2>&1
  echo "   Volume: $(find "$B/n8n-volume-$D.tgz" -printf '%s' 2>/dev/null || echo 0) Bytes"
fi

# 3. Aufbewahrung
find "$B" -name 'n8n-export-*.tgz' -mtime +14 -delete
find "$B" -name 'n8n-volume-*.tgz' -mtime +35 -delete
echo "$(date '+%F %T') Backup-Ende, belegt: $(du -sh "$B" | cut -f1)"
