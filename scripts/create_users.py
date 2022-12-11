from users.factories import UserFactory
from users.serializers import UserSerializer
from users_service import tasks
from users_service.celery import queue_rides, queue_notify, queue_reviews


def create(amount):
    for user in range(amount):
        user = UserFactory()
        tasks.publish_message(UserSerializer(user).data, 'users', queue_notify, 'notify')
        tasks.publish_message(UserSerializer(user).data, 'users', queue_rides, 'send')
        tasks.publish_message(UserSerializer(user).data, 'users', queue_reviews, 'review')
