from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="user-register"),
    path("register", views.register_user),
    path("login/", views.login_user, name="user-login"),
    path("login", views.login_user),
    path("logout/", views.logout_user, name="user-logout"),
    path("logout", views.logout_user),
]
