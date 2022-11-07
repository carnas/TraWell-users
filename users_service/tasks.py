from __future__ import absolute_import, unicode_literals

from celery import shared_task

from users_service.celery import app


@shared_task(name='rides')
def publish_message(message, title, queue, routing_key):
    body = {
        'title': title,
        'message': message
    }
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            body,
            exchange='trawell_exchange',
            queue=queue,
            routing_key=routing_key,
        )
