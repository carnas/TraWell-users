# Generated by Django 4.1.2 on 2022-10-21 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("date_of_birth", models.DateField()),
                (
                    "user_type",
                    models.TextField(
                        choices=[("private", "Private"), ("company", "Company")],
                        default="private",
                        max_length=7,
                    ),
                ),
                ("facebook", models.URLField(blank=True, default="")),
                ("instagram", models.URLField(blank=True, default="")),
                ("avatar", models.URLField(blank=True, default="")),
            ],
        ),
    ]