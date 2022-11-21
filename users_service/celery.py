from __future__ import absolute_import, unicode_literals

import logging
import os

import django
import kombu
from celery import Celery, bootsteps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_service.settings')
django.setup()

from users.models import User
from users.serializers import UserSerializer

app = Celery('users_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from . import tasks

# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='trawell_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue_users = kombu.Queue(
        name='users',
        exchange=exchange,
        routing_key='use',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic'
        },
        durable=True
    )
    queue_users.declare()

    queue_rides = kombu.Queue(
        name='rides',
        exchange=exchange,
        routing_key='send',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic'
        },
        durable=True
    )
    queue_rides.declare()

    queue_notify = kombu.Queue(
        name='notifications',
        exchange=exchange,
        routing_key='notify',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic'
        },
        durable=True
    )
    queue_notify.declare()

    queue_reviews = kombu.Queue(
        name='reviews',
        exchange=exchange,
        routing_key='review',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic'
        },
        durable=True
    )
    queue_reviews.declare()


# setting consumer
class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[queue_users],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        print(message)
        if body['title'] == 'avg_change':
            try:
                user = User.objects.get(user_id=body['message']['user_id'])
                user_data = {
                    'avg_rate': body['message']['avg_rate']
                }
                serializer = UserSerializer(user, data=user_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    tasks.publish_message(serializer.data, 'users', queue_notify, 'notify')
                    tasks.publish_message(serializer.data, 'users', queue_rides, 'send')

            except User.DoesNotExist:
                logging.error("User doesn't exist")

        message.ack()


app.steps['consumer'].add(MyConsumerStep)

