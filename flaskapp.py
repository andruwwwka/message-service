import logging.config

from flask.app import Flask

from sender.models import db
from sender.resources import api


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(api)
    return app


app = create_app("settings.stable")

logging.config.dictConfig(app.config["LOGGING"])

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])
