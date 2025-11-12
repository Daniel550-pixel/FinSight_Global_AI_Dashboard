#!/bin/bash
echo "[INFO] Git backup en safe restore..."
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    git add .
    git commit -m "Safe upgrade $(date '+%Y-%m-%d %H:%M:%S')" || echo "[INFO] Geen wijzigingen om te committen"
    git push origin master || echo "[WARNING] Push mislukt, controleer remote/rechten"
    echo "[INFO] Git backup voltooid."
else
    echo "[INFO] Geen Git repository gevonden, skip git backup."
fi
