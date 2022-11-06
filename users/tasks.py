from __future__ import absolute_import, unicode_literals

from celery import shared_task

from users_service.celery import app


@shared_task(name='notifications')
def publish_message_n(message):
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            message,
            exchange='trawell_exchange',
            queue='notifications',
            routing_key='notify.users',
        )


@shared_task(name='rides')
def publish_message(message):
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            message,
            exchange='trawell_exchange',
            queue='rides',
            routing_key='key.users',
        )

