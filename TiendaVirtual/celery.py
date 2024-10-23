import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TiendaVirtual.settings')

app = Celery('TiendaVirtual')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#app.conf.broker_url = 'amqp://guest:guest@localhost'