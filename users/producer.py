# import time
#
# import django
# import os
# import json
# import pika
# import logging
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "users_service.settings")
# django.setup()
#
# logger = logging.getLogger(__name__)
#
# parameters = pika.ConnectionParameters(host='localhost', port=5672,
#                                        heartbeat=600, blocked_connection_timeout=300)
# connection = pika.BlockingConnection(parameters)
#
# channel = connection.channel()
#
# channel.queue_declare(queue='users')
#
#
# def publish(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(exchange='', routing_key='users', body=json.dumps(body), properties=properties)
#     print('send message')
#     logger.info("Message was sent")
#
#
#
# # def publish(method, body):
# #     pass
