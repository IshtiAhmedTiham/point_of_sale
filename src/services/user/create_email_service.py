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


def send_email(
    to: str,
    subject: str,
    body: str
):
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

        print(f"Email successfully sent to : {to}")

    except Exception as error:
        print(f"Email sent successfully fail: {to}")


def send_user_email(user):
    with open("src/template/user/create_user_mail.html", "r") as file:
        body = file.read()

    body = body.replace("{{ user.name }}", user.name)
    body = body.replace("{{ user.email }}", user.email)
    body = body.replace("{{ user.phone }}", user.phone)
    body = body.replace("{{ user.role }}", user.role)
    body = body.replace("{{ user.status }}", user.status)

    return send_email(
        to=user.email,
        subject="Your Account is Successfully Created",
        body=body
    )
