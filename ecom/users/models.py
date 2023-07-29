from django.db import models
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator


class User(models.Model):
    username = models.CharField(
        max_length=30, unique=True, validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")]
    )
    first_name = models.CharField(
        "first name",
        max_length=30,
        validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")],
    )
    last_name = models.CharField(
        "last name", max_length=30, validators=[RegexValidator(r"^[a-zA-Z0-9_]+$")]
    )
    password = models.BinaryField(max_length=60)
    email = models.CharField(max_length=50, unique=True, validators=[EmailValidator()])

    def __str__(self) -> str:
        return self.username


class History(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField("item name", max_length=50)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    total = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return self.username + ": " + self.item_name
