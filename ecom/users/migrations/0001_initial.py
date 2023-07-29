# Generated by Django 4.2.3 on 2023-07-28 05:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=30)),
                (
                    "first_name",
                    models.CharField(max_length=30, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=30, verbose_name="last name"),
                ),
                ("password", models.CharField(max_length=30)),
                ("email", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item_name",
                    models.CharField(max_length=50, verbose_name="last name"),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "total",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.user"
                    ),
                ),
            ],
        ),
    ]
