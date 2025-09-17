# app/emailer.py
import smtplib
from email.mime.text import MIMEText
from threading import Thread
from .config import config

def send_email(subject, body, to_email):
    """Send email synchronously"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['EMAIL_FROM']
    msg['To'] = to_email

    try:
        with smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT']) as server:
            server.starttls()
            server.login(config['SMTP_USER'], config['SMTP_PASSWORD'])
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def send_email_background(account):
    """Send account creation email in a background thread"""
    subject = "New Account Created"
    body = f"Account {account.name} ({account.number}) with balance {account.balance} created."
    to_email = config['EMAIL_TO']   # 👈 send to Maheshwaran instead of yourself
    Thread(target=send_email, args=(subject, body, to_email)).start()
