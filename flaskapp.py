import logging.config
import os

from flask.app import Flask

from sender.celery_app import init_celery, celery_app
from sender.models import db
from sender.resources import api


def create_app(config=None):
    app = Flask(__name__)

    config = config or os.environ.setdefault("FLASK_SETTINGS_MODULE", "settings/development.py")
    app.config.from_pyfile(config)
    db.init_app(app)
    app.register_blueprint(api)

    init_celery(app, celery_app)

    return app


app = create_app()

logging.config.dictConfig(app.config["LOGGING"])

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])
