import celery

app = celery.Celery('tipsetc')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()