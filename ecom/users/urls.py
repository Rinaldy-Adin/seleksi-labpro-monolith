from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("catalog/", views.ItemListView.as_view(), name="catalog"),
    path("history/", views.HistoryListView.as_view(), name="history"),
    path("detail/<str:item_id>/", views.ItemDetail, name="detail"),
    path("buy/<str:item_id>/", views.BuyView.as_view(), name="buy"),
]
