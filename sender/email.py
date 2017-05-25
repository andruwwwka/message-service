import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flaskapp import app
from sender.celery import celery_logger


class Email(object):
    """Класс транспорта Email сообщений

    """

    @staticmethod
    def send(message):
        """Метод отправки сообщения

        :param message: объект сообщения
        :return: True
        """
        result = True
        from_mail = app.config["EMAIL_SENDER"]
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.header
        msg["From"] = from_mail
        part = MIMEText(message.body, "html" if message.type == "html" else "plain")
        msg.attach(part)
        smtp = smtplib.SMTP(app.config["SMTP_SERVER"], app.config["SMTP_PORT"])
        smtp.starttls()
        smtp.login(from_mail, app.config["EMAIL_PASSWORD"])
        celery_logger.info("Отправка сообщения %s адресату %s" % (message.id, message.recipient))
        msg["To"] = message.recipient
        try:
            smtp.sendmail(from_mail, message.recipient, msg.as_string())
            celery_logger.info("Сообщение %s отправлено адресату %s" % (message.id, message.recipient))
        except BaseException:
            result = False
            celery_logger.error("Произошла ошибка при отправке сообщения %s адресату %s" % (message.id, message.recipient))
        smtp.quit()
        return result
