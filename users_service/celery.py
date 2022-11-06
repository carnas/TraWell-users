from __future__ import absolute_import, unicode_literals

import os

import django
import kombu
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_service.settings')
django.setup()

app = Celery('users_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='trawell_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    # queue_notify = kombu.Queue(
    #     name='notifications',
    #     exchange=exchange,
    #     routing_key='notify.*',
    #     channel=conn,
    #     message_ttl=600,
    #     queue_arguments={
    #         'x-queue-type': 'classic'
    #     },
    #     durable=True
    # )
    # queue_notify.declare()

    # queue = kombu.Queue(
    #     name='rides',
    #     exchange=exchange,
    #     routing_key='key.#',
    #     channel=conn,
    #     message_ttl=600,
    #     queue_arguments={
    #         'x-queue-type': 'classic'
    #     },
    #     durable=True
    # )
    # queue.declare()
