import json
import logging

from flask import render_template, request
from flask.blueprints import Blueprint
from mongoengine import ValidationError

from sender.models import Message

api = Blueprint(__name__, "api")


@api.route("/", methods=["GET"])
def index():
    """Представление получения списка сообщений

    :return: рендер шаблона
    """
    page_num = int(request.args.get('page') or 1)
    per_page = int(request.args.get('per_page') or 10)
    msgs = Message.objects.order_by('-created').paginate(page=page_num, per_page=per_page)
    return render_template("index.html", messages=msgs, per_page=per_page)


@api.route("/message", methods=["GET"])
def message():
    """Представление API получения данных о сообщении

    :return: json объекта сообщения
    """
    result = json.dumps({"error": "Отсутствует обязательный GET параметр: идентификатор сообщения"})
    if request.args and request.args.get('message_id'):
        try:
            if Message.objects(id=request.args.get('message_id')):
                msg = Message.objects.get(id=request.args.get('message_id'))
                result = msg.to_json()
            else:
                result = json.dumps({"error": "Сообщение не найдено"})
        except ValidationError:
            result = json.dumps({"error": "Некорректный идентификатор сообщения"})
    return result

#review
@api.route("/messages", methods=["POST"])
def messages():
    """Представление API добавления сообщения

    :return: результат обработки запроса
    """
    response = "В вашем POST запросе отсутствуют данные"
    if request.json:
        post_data = request.json
        try:
            idents = list()
            #review
            for recipient in post_data.get("recipients"):
                msg = Message(
                    type=post_data.get("type"),
                    header=post_data.get("header"),
                    body=post_data.get("body"),
                    format=post_data.get("format"),
                    tags=post_data.get("tags"),
                    recipient=recipient
                )
                msg.save()
                from sender.tasks import send_message
                send_message.delay(str(msg.id))
                idents.append(str(msg.id))
                logging.info("Создано сообщение с идентификатором %s из запроса %s" % (msg.id, request.json))
            #review
            response = "Идентификаторы новых сообщений: %s" % ", ".join(idents)
        except ValidationError:
            logging.warning("Отклонен запрос на добавление сообщения с параметрами %s" % request.json)
            response = "POST запрос содержит невалидные данные"
    return response
