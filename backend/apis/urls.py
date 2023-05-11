from django.urls import path
from . import views

urlpatterns = [
    path("getfeed", views.getfeed, name="getfeed"),
    path("log", views.getlog, name="getlog"),
    path("chat", views.getchat, name="getchat"),
    path("user", views.getchat, name="getuser"),

    path("img", views.getimg, name="getimg"),
    path("action", views.action, name="action"),
]
