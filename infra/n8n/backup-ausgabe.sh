#!/usr/bin/env bash
# Erzwungener Befehl für den Mac-Backup-Schlüssel (authorized_keys: command=…,restrict).
# Gibt nur das neueste Backup als Datenstrom aus – sonst nichts.
#   ssh … export   → neuester täglicher Export
#   ssh … volume   → neuester Volume-Abzug
#   ssh … liste    → Dateinamen und Größen
set -euo pipefail
B=/root/backup/n8n
case "${SSH_ORIGINAL_COMMAND:-}" in
  export) exec cat "$(ls -t "$B"/n8n-export-*.tgz | head -1)" ;;
  volume) exec cat "$(ls -t "$B"/n8n-volume-*.tgz | head -1)" ;;
  liste)  ls -lt "$B" | awk 'NR>1{print $5, $9}' ;;
  *) echo "erlaubt: export | volume | liste" >&2; exit 2 ;;
esac
