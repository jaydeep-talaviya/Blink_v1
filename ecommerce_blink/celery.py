from celery import Celery
from django.conf import settings
import os
import django

# Create default Celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_blink.settings')

app = Celery('ecommerce_blink',broker_url=settings.CELERY_BROKER_URL)
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

# namespace='CELERY' means all celery-related configuration keys
# should be uppercased and have a `CELERY_` prefix in Django settings.
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
app.config_from_object("django.conf:settings")
app.conf.beat_schedule = {
}
# When we use the following in Django, it loads all the <appname>.tasks
# files and registers any tasks it finds in them. We can import the
# tasks files some other way if we prefer.
app.autodiscover_tasks(settings.INSTALLED_APPS)