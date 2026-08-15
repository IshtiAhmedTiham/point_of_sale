import os
import smtplib
from email.mime.text import MIMEText

EMAIL_CONFIG = {
    "sender" : os.getenv("EMAIL_SENDER"),
    "password" : os.getenv("EMAIL_PASSWORD"),
    "server" : os.getenv("SMTP_SERVER"),
    "port" : os.getenv("SMTP_PORT",587)
}

def send_email(to : str, subject : str ,body : str):
    msg = MIMEText(body)
    msg["From"] = EMAIL_CONFIG["sender"]
    msg["To"] = to
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP(EMAIL_CONFIG["server"], EMAIL_CONFIG["port"])
        server.starttls()
        server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
        server.send_message(msg)

        print(f"Email Successfully Send in {to}")
        
    except Exception as error:
        print(f"{error}")

def send_brand_email(brand):
    body = "Your account is successfully created"

    return send_email(
        to = brand.email,
        subject = f"Welcome, {brand.name}",
        body = body
    )


