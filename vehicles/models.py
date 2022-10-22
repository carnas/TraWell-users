from django.db import models

from users.models import User


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
