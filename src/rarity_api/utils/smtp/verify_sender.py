from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from rarity_api.settings import settings


class MailSender:

    def __init__(self):
        pass


    @staticmethod
    async def send_verify_link(email: str, token: str):
        smtp_server = 'smtp.mail.ru'
        smtp_port = 587

        smtp_username = settings.mail_email
        smtp_password = settings.mail_password

        from_addr = settings.mail_email
        to_addr = email
        # Отправитель и получатель

        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = "Подтверждение регистрации"

        
        # Текст сообщения
        url = f"{settings.api_base_url}/verification/verify?token={token}"
        msg.attach(MIMEText(f"Здравствуйте!\nНажмите на ссылку для подтверждения почты: {url}"))
        
        result = None

        # Отправка сообщения
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
        except Exception as e:
            ...
        finally:
            server.quit()
            return result