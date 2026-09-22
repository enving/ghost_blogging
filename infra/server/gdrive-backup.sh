#!/usr/bin/env bash
# Server-Backups verschlüsselt nach Google Drive (rclone crypt über drive.file-Zugriff).
# Liegt als /opt/server-backup/gdrive-backup.sh, Cron: /etc/cron.d/server-backup.
#   gdrive-backup.sh n8n      täglich: neue n8n-Exporte/-Images aus /root/backup/n8n hochladen
#   gdrive-backup.sh system   wöchentlich: Voll-Backup des ganzen Servers streamen + prüfen
#   gdrive-backup.sh status   Belegung und vorhandene Stände anzeigen
# Remote "gcrypt:" = verschlüsselter Ordner "vps-backup" im Drive. Ohne das crypt-Passwort
# (Mac-Schlüsselbund: server-backup-crypt) sind die Dateien nicht lesbar – auch nicht für Google.
set -euo pipefail
export RCLONE_CONFIG=/root/.config/rclone/rclone.conf
D=$(date +%F)
log() { echo "$(date '+%F %T') $*"; }

case "${1:-}" in
  n8n)
    rclone copy /root/backup/n8n gcrypt:n8n --max-age 8d
    rclone delete gcrypt:n8n --min-age 60d
    log "n8n: hochgeladen, $(rclone size gcrypt:n8n --json | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["count"], "Dateien,", round(d["bytes"]/1e6), "MB")')"
    ;;
  system)
    F="system/vps-system-$D.tar.gz"
    log "system: Start"
    SSH_ORIGINAL_COMMAND=system /opt/n8n/backup-ausgabe.sh | rclone rcat "gcrypt:$F"
    # Prüfen statt glauben: Archiv zurücklesen und vollständig testen
    if rclone cat "gcrypt:$F" | gzip -t; then
      log "system: $F geprüft, $(rclone size "gcrypt:$F" --json | python3 -c 'import sys,json;print(round(json.load(sys.stdin)["bytes"]/1e9,2))') GB"
      # Aufbewahrung: die letzten 4 Wochen
      rclone delete gcrypt:system --min-age 27d
    else
      log "!! system: $F ist beschädigt – gelöscht, ältere Stände bleiben"
      rclone deletefile "gcrypt:$F" || true
      exit 1
    fi
    ;;
  status)
    rclone about gdrive: 2>/dev/null | grep -E 'Total|Used|Free' || true
    rclone lsl gcrypt: 2>/dev/null | awk '{printf "%8.1f MB  %s\n", $1/1e6, $4}' | sort -k3
    ;;
  *) echo "Nutzung: gdrive-backup.sh n8n|system|status" >&2; exit 2 ;;
esac
