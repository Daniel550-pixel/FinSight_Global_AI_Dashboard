#!/bin/bash
echo "[INFO] Upgraden: Alerts..."
cat > alerts.py <<'EOALERT'
def send_alert(message):
    print(f"[ALERT] {message}")
EOALERT
echo "[INFO] Alerts module toegevoegd."
