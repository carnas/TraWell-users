import datetime

from users.models import User
from vehicles.models import Vehicle
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer
from users_service import tasks
from users_service.celery import queue_rides, queue_notify, queue_reviews

users = [
    {'first_name': 'Anna',
     'last_name': 'Nowak',
     'email': 'anna.nowak@wp.pl',
     'date_of_birth': datetime.date(2000, 6, 28),
     'avg_rate': 3.5,
     'user_type': 'private',
     'facebook': 'https://www.facebook.com/',
     'instagram': '',
     'avatar': ''}
]


vehicles = [
    {'make': 'ford',
     'model': 'mustang',
     'color': 'black',
     'user_email': 'anna.nowak@wp.pl'}  # must be in db
]


def create_manual_users(users):
    for user in users:
        new_user = User.objects.create(first_name=user['first_name'],
                                       last_name=user['last_name'],
                                       email=user['email'],
                                       date_of_birth=user['date_of_birth'],
                                       avg_rate=user['avg_rate'],
                                       user_type=user['user_type'],
                                       facebook=user['facebook'],
                                       instagram=user['instagram'],
                                       avatar=user['avatar'])
        new_user.save()
        serializer = UserSerializer(new_user)
        tasks.publish_message(serializer.data, 'users', queue_notify, 'notify')
        tasks.publish_message(serializer.data, 'users', queue_rides, 'send')
        tasks.publish_message(serializer.data, 'users', queue_reviews, 'review')


def create_manual_vehicles(vehicles):
    for vehicle in vehicles:
        user = User.objects.get(email=vehicle['user_email'])
        new_vehicle = Vehicle.objects.create(make=vehicle['make'],
                                             model=vehicle['model'],
                                             color=vehicle['color'],
                                             user=user)
        new_vehicle.save()
        tasks.publish_message(VehicleSerializer(vehicle).data, "vehicles.create", queue_rides, 'send')


create_manual_users(users)
create_manual_vehicles(vehicles)