import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_CONFIG = {
    "sender": os.getenv("EMAIL_SENDER"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "server": os.getenv("SMTP_SERVER"),
    "port": int(os.getenv("SMTP_PORT", 587))
}


def send_email(to: str,subject: str,body: str):
    msg = MIMEMultipart()

    msg["From"] = "No Reply"
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(EMAIL_CONFIG["server"], EMAIL_CONFIG["port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
            server.send_message(msg)

        print(f"Email successfully sent to {to}")

    except Exception as error:
        print(f"Email sending successfully failed: {error}")


def send_brand_email(brand):
    with open("src/template/brand/create_brand_register_mail.html", "r") as file:
        body = file.read()

    body = body.replace("{{ brand_name }}", brand.name)
    body = body.replace("{{ brand_email }}", brand.email)
    body = body.replace("{{ brand_status }}",brand.status)

    return send_email(
        to=brand.email,
        subject="Your brand registration is complete",
        body=body
    )