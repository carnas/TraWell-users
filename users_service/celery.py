from __future__ import absolute_import, unicode_literals
import django
import os
import kombu
import json
from celery import Celery, bootsteps

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

    queue = kombu.Queue(
        name='notifications',
        exchange=exchange,
        routing_key='key.#',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()

    queue = kombu.Queue(
        name='rides',
        exchange=exchange,
        routing_key='key.#',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()


# setting consumer
# class MyConsumerStep(bootsteps.ConsumerStep):
#
#     def get_consumers(self, channel):
#         print('get consumers')
#         return [kombu.Consumer(channel,
#                                queues=[queue],
#                                callbacks=[self.handle_message],
#                                accept=['json'])]
#
#     def handle_message(self, body, message):
#         print('handle_message')
#         # ride_data = json.loads(body)
#         print('Received message: {0!r}'.format(body))
#         if 'ride_id' in body:
#             print(body['ride_id'])
#             ride = Ride.objects.get(ride_id=body['ride_id'])
#             print('----------------------------------------')
#             print(ride)
#             print('----------------------------------------')
#         else:
#             print('To nie ride')
#         message.ack()
#
#
# app.steps['consumer'].add(MyConsumerStep)
