from sender.celery_app import celery_logger
from sender.email_transport import Email
from sender.models import Message
from sender.telegram import Telegram


class Transport(object):
    """Общий класс транспорта для менеджмента сообщений

    """

    # Используемые транспорты для отправки сообщений
    transports = {
        "email": Email,
        "telegram": Telegram
    }

    def __init__(self, message_id):
        """ Инициализация объекта транспорта

        :param message_id: идентификатор сообщения
        """
        self.message = Message.objects.get(id=message_id)
        self.transport = self.transports.get(self.message.type)

    def mark_message_process(self):
        """Подогтовка к отправке сообщения

        :return: True
        """
        self.message.status = "process"
        self.message.save()
        celery_logger.info("Начало обработки сообщения %s" % self.message.id)
        return True

    def mark_message_sent(self, sended):
        """Фиксация отправки сообщения

        :return: True
        """
        self.message.status = "sent" if sended else "error"
        self.message.save()
        celery_logger.info("Обработка сообщения %s закончена" % self.message.id)
        return True

    def send(self):
        """Метод отправки сообщения

        :return: результат отправки
        """
        try:
            self.mark_message_process()
            sended = self.transport.send(self.message)
            self.mark_message_sent(sended)
            return sended
        except Exception as e:
            celery_logger.exception("Exception processing %s", self.message)
            raise e
