import jwt
import os

from django.http import HttpResponseForbidden, HttpRequest
from django.urls import reverse
from django.shortcuts import redirect


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        excluded_paths = [
            reverse("users:login"),
            reverse("users:register"),
        ]

        if request.path.startswith("/admin/") or request.path == "/admin":
            response = self.get_response(request)
            return response

        if "AUTH_TOKEN" not in request.COOKIES and request.path in excluded_paths:
            response = self.get_response(request)
            return response

        token = request.COOKIES.get("AUTH_TOKEN")
        secret_key = os.environ.get("SECRET_KEY")

        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return redirect(reverse("users:login"), status=401)
        except jwt.InvalidTokenError:
            return redirect(reverse("users:login"), status=401)

        if request.path in excluded_paths:
            return redirect(reverse("users:catalog"))

        request.user = {"username": decoded_token["username"]}

        response = self.get_response(request)
        return response
