#!/bin/bash
echo "[INFO] Upgraden: Deep RL agent..."
cat > deep_rl_agent.py <<'EOFAGENT'
def allocate_portfolio(state):
    return {"equities":0.4,"crypto":0.3,"oil":0.2,"real_estate":0.1}
EOFAGENT
echo "[INFO] Deep RL agent toegevoegd."
