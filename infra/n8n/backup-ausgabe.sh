#!/usr/bin/env bash
# Erzwungener Befehl für den Mac-Backup-Schlüssel (authorized_keys: command=…,restrict).
# Gibt nur Backups als Datenstrom aus – sonst nichts. Gegenstück: ~/Documents/Dev/server
#   ssh … export   → neuester täglicher n8n-Export
#   ssh … volume   → neuester n8n-Volume-Abzug
#   ssh … system   → Voll-Backup des ganzen Servers (tar.gz aller Dateien + MySQL-Dump), live erzeugt
#   ssh … liste    → vorhandene n8n-Backups
set -euo pipefail
B=/root/backup/n8n
case "${SSH_ORIGINAL_COMMAND:-}" in
  export) exec cat "$(ls -t "$B"/n8n-export-*.tgz | head -1)" ;;
  volume) exec cat "$(ls -t "$B"/n8n-volume-*.tgz | head -1)" ;;
  liste)  ls -lt "$B" | awk 'NR>1{print $5, $9}' ;;
  system)
    # 1. Konsistenter Dump aller MySQL-Datenbanken (Ghost) – landet im Archiv unter /root/backup/system
    S=/root/backup/system
    mkdir -p "$S" && chmod 700 "$S"
    if command -v mysqldump >/dev/null && [ -f /etc/mysql/debian.cnf ]; then
      mysqldump --defaults-file=/etc/mysql/debian.cnf --all-databases --single-transaction \
        --routines --events 2>/dev/null | gzip -1 > "$S/mysql-all.sql.gz" || echo "!! mysqldump fehlgeschlagen" >&2
    else
      echo "!! kein mysqldump/debian.cnf – Datenbank nur als Rohdateien im Archiv" >&2
    fi
    dpkg --get-selections > "$S/paketliste.txt" 2>/dev/null || true
    # 2. Ganzes Dateisystem streamen. --one-file-system lässt /proc, /sys, /dev, /run weg.
    #    Niedrige Priorität, damit Ghost und n8n weiter antworten.
    cd /
    set +e
    nice -n 19 ionice -c3 tar --one-file-system --numeric-owner --acls --xattrs -cpf - \
      --warning=no-file-changed --warning=no-file-removed --ignore-failed-read \
      --exclude=./swapfile --exclude=./var/lib/docker/overlay2 --exclude=./var/lib/docker/image \
      --exclude=./var/lib/docker/buildkit --exclude=./var/cache/apt/archives \
      --exclude=./tmp --exclude=./var/tmp --exclude=./root/backup/n8n \
      --exclude=./var/lib/mysql/'#innodb_temp' \
      . | nice -n 19 gzip -1
    rc=${PIPESTATUS[0]}
    # tar-Exit 1 = Dateien haben sich beim Lesen geändert (Logs usw.) – unkritisch
    [ "$rc" -le 1 ] || exit "$rc"
    ;;
  *) echo "erlaubt: export | volume | system | liste" >&2; exit 2 ;;
esac
