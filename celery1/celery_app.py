from celery import Celery

app = Celery('app',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')
app.autodiscover_tasks(['celery1.tasks'])
