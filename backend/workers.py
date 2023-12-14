from celery import Celery
from flask import current_app as app

celery = Celery('Application Jobs')

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

broker_url = 'redis://localhost:6379/1'  # Update with your Redis broker URL
result_backend = 'redis://localhost:6379/2'  # Update with your Redis result backend URL

celery.conf.update(
    broker_url=broker_url,
    result_backend=result_backend
)

from task import *