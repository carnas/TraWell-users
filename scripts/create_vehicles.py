import random

from vehicles.factories import VehicleFactory
from users.models import User


def create(amount):
    users = User.objects.all()
    for vehicle in range(amount):
        user_index = random.choice(range(len(users)))
        VehicleFactory(user=users[user_index])