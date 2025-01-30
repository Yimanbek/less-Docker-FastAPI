import smtplib
from email.mime.text import MIMEText
from .config_send_email import settings

def send_message_to_client(email: str, warning = False, time = None):

    if warning:
        subject = "Ваша запись на сегодня, наш сервис BarberShop"
        body = f"""Здраствуйте ваш запись сегодня на время - {time}"""
    else:
        subject = "Вы записались на наш сервис BarberShop"
        body = f"""Здравствуйте! вы записаны на веремя - {time},
        
    Спасибо, что выбрали нас!"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()  
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Письмо отправлено на {email}")

    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

