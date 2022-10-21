from django.db import models

from users.models import User


class Vehicle(models.Model):
    make = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    color = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
