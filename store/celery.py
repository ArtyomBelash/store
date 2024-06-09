import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
app = Celery('store')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(
    broker_url='amqp://guest:guest@localhost',
    result_backend='rpc://',
    task_track_started=True,
    task_time_limit=300,
    task_soft_time_limit=270,
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(task_name)s[%(task_id)s]: %(message)s',
)
