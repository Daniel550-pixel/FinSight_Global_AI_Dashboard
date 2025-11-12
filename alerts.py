import os
import smtplib
from slack_sdk import WebhookClient

def send_slack(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        webhook = WebhookClient(webhook_url)
        webhook.send(text=message)

def send_email(subject, message):
    server = os.getenv("EMAIL_SMTP_SERVER")
    port = int(os.getenv("EMAIL_SMTP_PORT", 587))
    user = os.getenv("EMAIL_SMTP_USER")
    password = os.getenv("EMAIL_SMTP_PASSWORD")
    if all([server, user, password]):
        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.sendmail(user, user, f"Subject: {subject}\n\n{message}")
