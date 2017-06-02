MONGODB_SETTINGS = {'db': 'testing',}
TESTING = True
SECRET_KEY = 'flask+mongoengine=<3'
debug = True

HOST = "127.0.0.1"
PORT = 5000

# Настройки логера
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s][%(filename)s:%(lineno)s] %(name)s: %(message)s'
        }
    },

    'handlers': {
        'default': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },

    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Настройки Celery
CELERY_MAIN_MODULE = "sender"
CELERY_RESULT_BACKEND = "amqp://"
CELERY_BROKER_URL = "amqp://"
CELERY_TASKS_MODULES = ["sender.tasks"]

# Настройки сервера отправки Email
SMTP_SERVER = ""
SMTP_PORT = 0
EMAIL_PASSWORD = ""
EMAIL_SENDER = ""

# Настройки Telegram Bot'a
TELEGRAM_BOT_TOKEN = ""
