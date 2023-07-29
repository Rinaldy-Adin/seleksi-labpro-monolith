from typing import Any, Dict
import requests
import os
from urllib.parse import urljoin
import jwt
import bcrypt

from django import http
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from django.conf import settings

from .models import User, History
from .forms import LoginForm, RegisterForm


class LoginView(TemplateView):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        return render(request, "login.html")

    def post(self, request: http.HttpRequest, *args: Any, **kwargs: Any):
        form = LoginForm(request.POST)
        if not form.is_valid():
            errors = []
            for field in form:
                for error in field.errors:
                    errors.append(field.name + ": " + error)
            return render(
                request,
                "login.html",
                {"error_messages": errors},
            )

        try:
            user = User.objects.get(username=request.POST["username"])
        except (KeyError, User.DoesNotExist):
            return render(request, "login.html", {"error_messages": ["User not found"]})
        else:
            if not bcrypt.checkpw(
                request.POST["password"].encode("utf8"), user.password
            ):
                return render(
                    request, "login.html", {"error_messages": ["Incorrect password"]}
                )

            payload = {"username": user.username}
            token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")

            response = redirect(reverse("users:catalog"))
            response.set_cookie("AUTH_TOKEN", token, httponly=True)

            return response


def LogoutView(request):
    response = redirect("users:login")
    response.set_cookie("AUTH_TOKEN", "", expires="Thu, 01 Jan 1970 00:00:00 GMT")
    return response


class RegisterView(TemplateView):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        return render(request, "register.html")

    def post(self, request: http.HttpRequest, *args: Any, **kwargs: Any):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            errors = []
            for field in form:
                for error in field.errors:
                    errors.append(field.name + ": " + error)
            return render(
                request,
                "register.html",
                {"error_messages": errors},
            )

        try:
            post = request.POST
            hashed_password = bcrypt.hashpw(
                post["password"].encode("utf8"), bcrypt.gensalt()
            )
            user = User(
                username=post["username"],
                email=post["email"],
                first_name=post["first_name"],
                last_name=post["last_name"],
                password=hashed_password,
            )
            user.save()
        except KeyError:
            return render(
                request, "register.html", {"error_messages": ["Form not complete"]}
            )
        else:
            return HttpResponseRedirect(reverse("users:login"))


class ItemListView(ListView):
    context_object_name = "item_list"
    template_name = "catalog.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        headers = {"Authorization": settings.BE_AUTH_TOKEN}
        response = requests.get(
            urljoin(os.environ.get("BE_SERVICE_URL"), "/barang"), headers=headers
        )
        data = response.json()["data"]

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navbar"] = "Catalog"
        context["username"] = self.request.user["username"]
        return context


def ItemDetail(request: http.HttpRequest, item_id):
    headers = {"Authorization": settings.BE_AUTH_TOKEN}

    response = requests.get(
        urljoin(os.environ.get("BE_SERVICE_URL"), "/barang/" + item_id), headers=headers
    )
    data = response.json()["data"]

    return render(
        request,
        "detail.html",
        {"item_detail": data, "username": request.user["username"]},
    )


class BuyView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        headers = {"Authorization": settings.BE_AUTH_TOKEN}

        response = requests.get(
            urljoin(os.environ.get("BE_SERVICE_URL"), "/barang/" + kwargs["item_id"]),
            headers=headers,
        )
        data = response.json()["data"]

        return render(
            request,
            "buy.html",
            {"item_detail": data, "username": request.user["username"]},
        )

    def post(self, request: http.HttpRequest, *args: Any, **kwargs: Any):
        headers = {"Authorization": settings.BE_AUTH_TOKEN}

        get_response = requests.get(
            urljoin(os.environ.get("BE_SERVICE_URL"), "/barang/" + kwargs["item_id"]),
            headers=headers,
        )
        data = get_response.json()["data"]

        post = request.POST

        if int(post["buy-qty"]) > data["stok"]:
            return render(
                request,
                "buy.html",
                {
                    "item_detail": data,
                    "error_messages": ["Insufficient item quantity available"],
                },
            )

        put_data = data.copy()
        put_data["stok"] -= int(post["buy-qty"])

        if put_data["stok"] != 0:
            mod_response = requests.put(
                urljoin(
                    os.environ.get("BE_SERVICE_URL"), "/barang/" + kwargs["item_id"]
                ),
                headers=headers,
                json=put_data,
            )
        else:
            mod_response = requests.delete(
                urljoin(
                    os.environ.get("BE_SERVICE_URL"), "/barang/" + kwargs["item_id"]
                ),
                headers=headers,
            )

        if mod_response.status_code == 200:
            user = User.objects.get(username=request.user["username"])
            history = History(
                username=user,
                item_name=put_data["nama"],
                quantity=int(post["buy-qty"]),
                total=int(post["buy-qty"]) * int(data["harga"]),
            )
            history.save(force_insert=True)
            return HttpResponseRedirect(reverse("users:catalog"))

        return HttpResponseRedirect(
            reverse("users:buy", kwargs={"item_id": data["id"]})
        )


class HistoryListView(ListView):
    template_name = "history.html"
    model = History
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return History.objects.filter(username__username=self.request.user["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navbar"] = "History"
        context["username"] = self.request.user["username"]
        return context
