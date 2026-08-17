import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_CONFIG = {
    "sender" : os.getenv("EMAIL_SENDER", ""),
    "password" : os.getenv("EMAIL_PASSWORD"),
    "smtp_server" : os.getenv("SMTP_SERVER"),
    "smtp_port" : os.getenv("SMTP_PORT", "587")
}


def send_email(to:str, subject:str, body:str):
    msg = MIMEMultipart()

    msg["Form"] = "No Reply"
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
            server.send_message(msg)

        print(f"Mail Successflly sent to : {to}")

    except Exception as error:
        print(f"Mail send successflly fail, Error : {error}")


def send_brand_email_for_delete(brand):
    with open("src/template/brand/delete_brand_register_mail.html", "r") as file:
        body = file.read()

    body = body.replace("{{ brand.name }}", brand.name)
    body = body.replace("{{ brand.email }}", brand.email)

    deleted_at = brand.deleted_at.strftime("%d %B %Y, %I:%M %p")
    body = body.replace("{{ deleted_at }}", deleted_at)

    return send_email(
        to=brand.email,
        subject="Your brand is successfully deleted",
        body=body
    )





    