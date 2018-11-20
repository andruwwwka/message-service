from sender.celery_app import celery_app

if __name__ == "__main__":
    from flaskapp import app
    celery_app.start()