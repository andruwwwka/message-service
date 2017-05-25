import json

import pytest
import requests
from bson import ObjectId

from flaskapp import create_app
from sender.models import Message


@pytest.fixture
def app():
    """Фикстура веб приложения

    :return: Flask приложение
    """
    application = create_app("settings.testing")
    return application


@pytest.fixture(scope="module")
def message():
    """Фикстура создания тестового сообщение

    :return: объект сообщения
    """
    msg = Message(
        type="email",
        header="Header of email",
        body="Message body",
        format="html",
        tags=["test1", "test2"],
        recipient="test@mail.ru"
    )
    msg.save()
    return msg


class TestMessageServer:
    """Тесты доступности локейшенов приложения

    """

    def test_server_is_alive(self, live_server):
        """Тест запуска сервера

        :param live_server: сервер
        :return: сервер запущен
        """
        assert live_server._process
        assert live_server._process.is_alive()

    def test_index_page_available(self, live_server):
        """Тест доступности главной страницы через GET запрос

        :param live_server: сервер
        :return: главная страница отдает 200 код ответа
        """
        res = requests.get(live_server.url("/"))
        assert res.status_code == 200

    def test_index_page_post_method_not_support(self, live_server):
        """Тест недоступности POST запроса на локейшен /

        :param live_server: сервер
        :return: сервер отдает 405 код ответа
        """
        res = requests.post(live_server.url("/"))
        assert res.status_code == 405

    def test_get_message_data_available(self, live_server):
        """Тест доступности локейшена получения данных о сообщении через GET запрос

        :param live_server: сервер
        :return: сервер отдает 200 код ответа
        """
        res = requests.get(live_server.url("/message"))
        assert res.status_code == 200

    def test_get_message_data_post_method_not_support(self, live_server):
        """Тест недоступности локейшена получения данных о сообщении через POST запрос

        :param live_server: сервер
        :return: сервер отдает 405 код ответа
        """
        res = requests.post(live_server.url("/message"))
        assert res.status_code == 405

    def test_post_message_data_available(self, live_server):
        """Тест доступности локейшена создания сообщений через POST запрос

        :param live_server: сервер
        :return: сервер отдает 200 код ответа
        """
        res = requests.post(live_server.url("/messages"))
        assert res.status_code == 200

    def test_post_message_data_get_method_not_support(self, live_server):
        """Тест недоступности GET запроса к локейшену создания сообщений

        :param live_server: сервер
        :return: сервер отдает 405 код ответа
        """
        res = requests.get(live_server.url("/messages"))
        assert res.status_code == 405


class TestMessageActions:
    """Тесты действий над сообщениями: получение, создание

    """

    def test_get_message_valid_data(self, live_server, message):
        """Тест получения сообщения с корректными параметрами

        :param live_server: сервер
        :param message: объект сообщения
        :return: статус ответа 200 & получен валидный json
        """
        res = requests.get(live_server.url("/message"), params={"message_id": message.id})
        assert res.status_code == 200 and json.loads(res.text) == json.loads(message.to_json())

    def test_get_message_without_data(self, live_server):
        """Тест получения данных о сообщении без передачи GET параметров

        :param live_server: сервер
        :return: статус ответа 200 & корректное сообщение об ошибке
        """
        res = requests.get(live_server.url("/message"))
        expected = json.dumps({"error": "Отсутствует обязательный GET параметр: идентификатор сообщения"})
        assert res.status_code == 200 and expected

    def test_get_message_invalid_message_id(self, live_server):
        """Тест получения данных о сообщении с передачей идентификатора несуществующего сообщения

        :param live_server: сервер
        :return: статус ответа 200 & корректное сообщение об ошибке
        """
        res = requests.get(live_server.url("/message"), params={"message_id": ObjectId()})
        expected = json.dumps({"error": "Сообщение не найдено"})
        assert res.status_code == 200 and expected

    def test_get_message_invalid_message_id_format(self, live_server):
        """Тест получения данных о сообщении с передачей идентификатора сообщения в невалидном формате

        :param live_server: сервер
        :return: статус ответа 200 & корректное сообщение об ошибке
        """
        res = requests.get(live_server.url("/message"), params={"message_id": "12"})
        expected = json.dumps({"error": "Некорректный идентификатор сообщения"})
        assert res.status_code == 200 and expected


    def test_post_message_correct_create(self, live_server):
        """Тест создания сообщений

        :param live_server: сервер
        :return: статус ответа 200 & корректное сообщение о результате & создались новые сообщения
        """
        count_message_before_add = Message.objects.count()
        data = {
            "type": "email",
            "header": "Msg header",
            "body": "Msg body",
            "format": "text",
            "recipients": ["test@mail.ru", "test@gmail.com"],
            "tags": ["tag1", "tag2"],
        }
        res = requests.post(live_server.url("/messages"), json=data)
        count_message_after_add = Message.objects.count()
        count_message_expected = count_message_before_add + len(data.get("recipients"))
        assert res.status_code == 200 and "Идентификаторы новых сообщений:" in res.text \
               and count_message_after_add == count_message_expected

    def test_post_message_empty_data(self, live_server):
        """Тест создания сообщений с отстуствующими данными в POST запросе

        :param live_server: сервер
        :return: статус ответа 200 & корректное сообщение об ошибке & новые сообщения не были созданы
        """
        count_message_before_add = Message.objects.count()
        res = requests.post(live_server.url("/messages"))
        count_message_after_add = Message.objects.count()
        assert res.status_code == 200 and "В вашем POST запросе отсутствуют данные" == res.text \
               and count_message_before_add == count_message_after_add

    def test_post_message_invalid_data(self, live_server):
        """Тест создания сообщений с передаваемыми невалидными данными (в POST данных нет типа сообщения)

        :param live_server: сервер
        :return: статус ответа 200 & корректное сообщение об ошибке & новые сообщения не были созданы
        """
        count_message_before_add = Message.objects.count()
        data = {
            "header": "Msg header",
            "body": "Msg body",
            "format": "text",
            "recipients": ["test@mail.ru", "test@gmail.com"],
            "tags": ["tag1", "tag2"],
        }
        res = requests.post(live_server.url("/messages"), json=data)
        count_message_after_add = Message.objects.count()
        assert res.status_code == 200 and "POST запрос содержит невалидные данные" == res.text \
               and count_message_before_add == count_message_after_add
