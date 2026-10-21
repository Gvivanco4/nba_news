import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(html: str, subject: str) -> None:
    sender = os.environ.get("SENDER_EMAIL")
    receipt = os.environ.get("RECEIPT_EMAIL")
    password = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("CONTRASEÑA_GMAIL")

    if not all((sender, receipt, password)):
        raise ValueError(
            "Configura SENDER_EMAIL, RECEIPT_EMAIL y GMAIL_APP_PASSWORD en tu entorno o .env"
        )

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receipt
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receipt, msg.as_string())


