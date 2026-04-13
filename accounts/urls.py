from django.urls import path
from .views import login_view, change_password, token_refresh_view

urlpatterns = [
    path("login", login_view, name="login"),
    path("change-password", change_password, name="change_password"),
    path("token/refresh", token_refresh_view, name="token_refresh")
]
