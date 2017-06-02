from pprint import pprint

#review
from celery import Celery
from flask.globals import current_app
from celery.utils.log import get_task_logger


def init_celery(app, celery):
    """Инициализация Celery

    :param celery:
    :type celery: Celery
    :return: Celery приложение
    """

    pprint(app.config)

    celery.config_from_object(dict(
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=app.config["CELERY_TASKS_MODULES"]
    ))

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = Celery(
    "sender",
    backend="redis://",
    broker="redis://",
    include=["sender.tasks"],

)

celery_logger = get_task_logger(__name__)
