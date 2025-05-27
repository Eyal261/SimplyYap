import os, ssl, smtplib
from dotenv import load_dotenv, find_dotenv
from email.message import EmailMessage

load_dotenv(find_dotenv(), override=True)

def send_contact_mail(name: str, sender_email: str, message_txt: str) -> None:
    msg = EmailMessage()
    msg["Subject"]  = f"Contact form → {name}"
    msg["From"]     = os.getenv("EMAIL_USER")
    msg["To"]       = os.getenv("EMAIL_USER")
    msg["Reply-To"] = sender_email
    msg.set_content(f"Name: {name}\nEmail: {sender_email}\n\n{message_txt}")

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)