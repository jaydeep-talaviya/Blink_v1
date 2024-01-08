# start_django_celery.py

from django.core.management.base import BaseCommand
from subprocess import Popen
from django.conf import settings


class Command(BaseCommand):
    help = 'Start Django server, Celery worker, and Celery Beat'

    def handle(self, *args, **options):
        worker_log_path = settings.CELERY_WORKER_LOG_PATH
        beat_log_path = settings.CELERY_BEAT_LOG_PATH

        # Start Celery worker
        worker_process = Popen(['celery', '-A', 'ecommerce_blink', 'worker', '-l', 'info'],
                               stdout=open(worker_log_path, 'w'), stderr=open(worker_log_path, 'a'))

        # Start Celery Beat
        beat_process = Popen(['celery', '-A', 'ecommerce_blink', 'beat', '-l', 'info'], stdout=open(beat_log_path, 'w'),
                             stderr=open(beat_log_path, 'a'))

        # Start Django server
        django_process = Popen(['python', 'manage.py', 'runserver'])

        # Wait for processes to complete
        worker_process.wait()
        beat_process.wait()
        django_process.wait()
