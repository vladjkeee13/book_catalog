from threading import Thread
from django.db.models.signals import post_save
from .models import Task

from catalog.management.commands.get_books import run_crawler


def handler_run_scraper(sender, instance, **kwargs):
    if kwargs.get('created'):
        try:
            start, end = instance.arg.split(',')
            start, end = int(start), int(end)
        except Exception as e:
            print(e, type(e))
            start, end = 100, 300
        Thread(target=run_crawler, args=(start, end, instance)).start()


post_save.connect(handler_run_scraper, sender=Task)
