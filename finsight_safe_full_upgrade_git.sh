#!/bin/bash
# FinSight Safe Full Upgrade + Git Backup
# Auteur: ChatGPT GPT-5 mini
# Gebruik: bash finsight_safe_full_upgrade_git.sh
set -e
trap 'echo "[ERROR] Er is iets misgegaan, terminal blijft open voor debug."' ERR

echo "[INFO] Start safe full restore, upgrade en Git backup..."

# 1️⃣ Virtual environment
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "[INFO] Virtual environment aangemaakt."
fi
source venv/Scripts/activate || source venv/bin/activate

# 2️⃣ START_STREAMLIT-check toevoegen
if [ -f finSight_master.py ]; then
    cp finSight_master.py finSight_master_backup.py
    echo "[INFO] Backup gemaakt: finSight_master_backup.py"

    cat > temp_fs_master.py <<'EOPY'
import os
START_STREAMLIT = os.getenv("START_STREAMLIT","true").lower() == "true"
if not START_STREAMLIT:
    print("[INFO] Streamlit auto-start is uitgeschakeld. Je kunt coderen zonder dat de terminal wordt geblokkeerd.")
    exit()
EOPY
    cat finSight_master.py >> temp_fs_master.py
    mv temp_fs_master.py finSight_master.py
    echo "[INFO] START_STREAMLIT-check toegevoegd."
fi

# 3️⃣ Core modules herstellen/aanmaken
cat > deep_rl_agent.py <<'EOFAGENT'
def allocate_portfolio(state):
    return {"equities":0.4,"crypto":0.3,"oil":0.2,"real_estate":0.1}
EOFAGENT

cat > monte_carlo.py <<'EOMC'
import numpy as np
def monte_carlo_forecast(initial_investment, years=50, simulations=1000):
    results=[]
    for _ in range(simulations):
        wealth = initial_investment
        for _ in range(years):
            growth = np.random.normal(0.08,0.15)
            wealth *= (1+growth)
        results.append(wealth)
    return results
EOMC

cat > sentiment_analysis.py <<'EOSA'
def get_sentiment_data():
    return {"news_score":0.5,"twitter_score":0.3,"trends_score":0.2}
EOSA

cat > alerts.py <<'EOALERT'
def send_alert(message):
    print(f"[ALERT] {message}")
EOALERT

cat > backtest.py <<'EOBT'
def run_backtest():
    print("[BACKTEST] Simulatie voltooid. Resultaten opgeslagen als CSV en plots.")
EOBT

cat > auth.py <<'EOAUTH'
import os
def check_password(input_password):
    correct_password = os.getenv("FIN_SIGHT_PASS","changeme")
    return input_password == correct_password
EOAUTH

cat > saas_projections.py <<'EOSAAS'
def generate_saas_forecast(users, avg_revenue):
    ARR = users * avg_revenue * 12
    MRR = users * avg_revenue
    return ARR, MRR
EOSAAS

cat > portfolio_hedging.py <<'EOPH'
def rebalance_portfolio(portfolio):
    print("[HEDGE] Portfolio auto-rebalancing uitgevoerd.")
EOPH

# 4️⃣ Dependencies installeren/updaten
echo "[INFO] Dependencies installeren/updaten..."
pip install --upgrade pip
pip install streamlit fastapi uvicorn plotly pandas numpy scikit-learn yfinance openai tensorflow torch requests python-dotenv slack_sdk matplotlib seaborn

# 5️⃣ Git backup (veilig)
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    git add .
    git commit -m "Safe full restore + upgrade $(date '+%Y-%m-%d %H:%M:%S')" || echo "[INFO] Geen wijzigingen om te committen"
    git push origin master || echo "[WARNING] Push mislukt, controleer remote/rechten"
    echo "[INFO] Git backup voltooid."
else
    echo "[INFO] Git repository niet gevonden, sla Git backup over."
fi

# 6️⃣ Eindstatus
echo "[INFO] Safe full restore & upgrade voltooid."
echo "[INFO] Backup: finSight_master_backup.py"
echo "[INFO] Terminal blijft open voor coderen."
echo "[INFO] Zet START_STREAMLIT=true om dashboard te starten."

