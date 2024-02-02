import os

import environ
from celery import Celery
from django.conf import settings

env = environ.Env().read_env(".env")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(packages=settings.INSTALLED_APPS)

BASE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

app.conf.broker_url = BASE_REDIS_URL
