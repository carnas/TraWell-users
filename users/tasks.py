from __future__ import absolute_import, unicode_literals

from celery import shared_task

from users_service.celery import app


@shared_task
def publish_message(message):
    with app.producer_pool.acquire(block=True) as producer:
        print('publishing on rides')
        producer.publish(
            message,
            exchange='trawell_exchange',
            queue='rides',
            routing_key='key.users',
        )


@shared_task
def publish_message_n(message):
    with app.producer_pool.acquire(block=True) as producer:
        print('publishing on notif')
        producer.publish(
            message,
            exchange='trawell_exchange',
            queue='notifications',
            routing_key='key.users2',
        )
