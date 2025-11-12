#!/bin/bash
echo "[INFO] Upgraden: Auth / wachtwoordbescherming..."
cat > auth.py <<'EOAUTH'
import os
def check_password(input_password):
    correct_password = os.getenv("FIN_SIGHT_PASS","changeme")
    return input_password == correct_password
EOAUTH
echo "[INFO] Auth module toegevoegd."
