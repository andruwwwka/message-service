import datetime
import textwrap

from flask_mongoengine import MongoEngine

db = MongoEngine()

# Допустимые типы сообщений
MESSAGE_TYPE = set((m_type,) * 2 for m_type in ["email", "telegram"])

# Допустимые форматы сообщений
FORMAT_TYPE = set((f_type,) * 2 for f_type in ["text", "html"])

# Допустимые статусы сообщений
MESSAGE_STATUSES = set((m_status,) * 2 for m_status in ["new", "process", "sent", "error"])


class Message(db.Document):
    """Модель сообщения

    """
    type = db.StringField(max_length=8, choices=MESSAGE_TYPE, required=True)
    header = db.StringField(max_length=1000, default="-")
    body = db.StringField(required=True)
    format = db.StringField(max_length=4, choices=FORMAT_TYPE, required=True)
    status = db.StringField(max_length=7, default="new", choices=MESSAGE_STATUSES)
    recipient = db.StringField(max_length=128, required=True)
    tags = db.ListField()
    created = db.DateTimeField(default=datetime.datetime.now)

    @property
    def tags_text(self):
        """Свойство объединения тегов сообщения в строку через запятую

        :return: строка с тегами сообщения
        """
        return ', '.join(self.tags)

    @property
    def short_tags_text(self):
        """Свойство получения сокращенной строки тегов

        :return: урезанная строка тегов
        """
        return textwrap.shorten(self.tags_text, width=40, placeholder="...")

    @property
    def date_of_creation(self):
        """Свойство получения даты сообщения в читабельном формате

        :return: строка даты
        """
        return self.created.strftime("%d.%m.%Y %H:%M:%S")

    @property
    def short_header(self):
        """Свойство получения сокращенного варианта заголовка сообщения

        :return: строа заголовка
        """
        return textwrap.shorten(self.header, width=40, placeholder="...")
