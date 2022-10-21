from django.db import models


class User(models.Model):
    class UserType(models.TextChoices):
        PRIVATE = "private"
        COMPANY = "company"

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    user_type = models.TextField(max_length=7, choices=UserType.choices, default=UserType.INDIVIDUAL)
    facebook = models.URLField(blank=True, default="")
    instagram = models.URLField(blank=True, default="")
    avatar = models.URLField(blank=True, default="")


