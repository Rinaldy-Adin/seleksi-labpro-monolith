# Generated by Django 4.2.3 on 2023-07-29 08:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_email_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="history",
            name="item_name",
            field=models.CharField(max_length=50, verbose_name="item name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[django.core.validators.EmailValidator()],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator("^[a-zA-Z0-9_]{3,20}$")
                ],
                verbose_name="first name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator("^[a-zA-Z0-9_]{3,20}$")
                ],
                verbose_name="last name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator("^[a-zA-Z0-9_]{3,20}$")
                ],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=30,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator("^[a-zA-Z0-9_]{3,20}$")
                ],
            ),
        ),
    ]
