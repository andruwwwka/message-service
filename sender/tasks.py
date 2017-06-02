from sender.celery_app import celery_app
from sender.transport import Transport


@celery_app.task
def send_message(message_id):
    """Задача отправки сообщения

    :param message_id: идентификатор сообщения
    :return: результат отправки
    """
    transport = Transport(message_id)
    return transport.send()
