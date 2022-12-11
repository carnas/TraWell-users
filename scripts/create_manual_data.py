import datetime

from users.models import User
from vehicles.models import Vehicle
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer, VehicleWithoutUserSerializer
from users_service import tasks
from users_service.celery import queue_rides, queue_notify, queue_reviews

users = [
    {'first_name': 'Olga',
     'last_name': 'Tokarczuk',
     'email': 'olga@tokarczuk.com',
     'date_of_birth': datetime.date(2000, 6, 28),
     'avg_rate': 3.5,
     'user_type': 'private',
     'facebook': 'https://www.facebook.com/',
     'instagram': '',
     'avatar': ''},
    {'first_name': 'Jan',
     'last_name': 'Kot',
     'email': 'jan@kot.com',
     'date_of_birth': datetime.date(1988, 2, 10),
     'avg_rate': 1.2,
     'user_type': 'company',
     'facebook': 'https://www.facebook.com/',
     'instagram': 'https://www.instagram.com/',
     'avatar': ''},
    {'first_name': 'Anna',
     'last_name': 'Sowa',
     'email': 'anna@sowa.com',
     'date_of_birth': datetime.date(1996, 12, 12),
     'avg_rate': 4.98,
     'user_type': 'private',
     'facebook': 'https://www.facebook.com/',
     'instagram': 'https://www.instagram.com/',
     'avatar': ''},
]

vehicles = [
    {'make': 'Opel',
     'model': 'Astra',
     'color': 'fast black',
     'user_email': 'olga@tokarczuk.com'},
    {'make': 'Ford',
     'model': 'Multipla',
     'color': 'baby blue',
     'user_email': 'olga@tokarczuk.com'}  # must be in db
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
        tasks.publish_message(VehicleSerializer(new_vehicle).data, "vehicles.create", queue_rides, 'send')


create_manual_users(users)
create_manual_vehicles(vehicles)
