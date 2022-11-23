import random

from users_service import tasks
from users_service.celery import queue_rides
from vehicles.factories import VehicleFactory
from users.models import User
from vehicles.serializers import VehicleSerializer


def create(amount):
    users = User.objects.all()
    for vehicle in range(amount):
        user_index = random.choice(range(len(users)))
        vehicle = VehicleFactory(user=users[user_index])
        tasks.publish_message(VehicleSerializer(vehicle).data, "vehicles.create", queue_rides, 'send')
