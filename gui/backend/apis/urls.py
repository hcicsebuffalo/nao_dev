from django.urls import path
from . import views

urlpatterns = [
    path("getfeed", views.getfeed, name="getfeed")
]
