FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install streamlit fastapi uvicorn plotly pandas numpy scikit-learn yfinance openai matplotlib seaborn requests python-dotenv
EXPOSE 8501
ENTRYPOINT ["streamlit","run","finSight_master.py","--server.port=8501","--server.address=0.0.0.0"]
