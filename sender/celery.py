from celery import Celery
from celery.utils.log import get_task_logger

from flaskapp import app


def make_celery(app):
    """Инициализация Celery

    :param app: Flask-приложение
    :return: Celery приложение
    """
    celery = Celery(
        app.config["CELERY_MAIN_MODULE"],
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=app.config["CELERY_TASKS_MODULES"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery_app = make_celery(app)
celery_logger = get_task_logger(__name__)

if __name__ == '__main__':
    celery_app.start()
