#!/bin/bash
echo "[INFO] Dependencies installeren/updaten..."
source venv/Scripts/activate || source venv/bin/activate
pip install --upgrade pip
pip install streamlit fastapi uvicorn plotly pandas numpy scikit-learn yfinance openai tensorflow torch requests python-dotenv slack_sdk matplotlib seaborn
echo "[INFO] Dependencies up-to-date."
