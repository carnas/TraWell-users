from django.db import models


class User(models.Model):

    class UserType(models.TextChoices):
        INDIVIDUAL = 'Individual'
        COMPANY = 'Company'

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    user_type = models.TextField(max_length=20, choices=UserType.choices, default=UserType.INDIVIDUAL)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


