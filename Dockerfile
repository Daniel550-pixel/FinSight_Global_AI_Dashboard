FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && \
    pip install streamlit fastapi uvicorn plotly pandas numpy scikit-learn yfinance openai tensorflow torch matplotlib seaborn python-dotenv slack_sdk
EXPOSE 8501
CMD ["streamlit", "run", "finSight_master.py", "--server.port=8501", "--server.address=0.0.0.0"]
