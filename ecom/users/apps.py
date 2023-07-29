import requests
import os
from urllib.parse import urljoin

from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        response = requests.post(
            urljoin(os.environ.get("BE_SERVICE_URL"), "login"),
            json={
                "username": os.environ.get("BE_SERVICE_UNAME"),
                "password": os.environ.get("BE_SERVICE_PASS"),
            },
        )
        settings.BE_AUTH_TOKEN = response.json()["data"]["token"]
        return super().ready()
