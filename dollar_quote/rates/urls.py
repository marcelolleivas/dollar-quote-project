from django.urls import path

from . import views

urlpatterns = [
    path("rates", views.index, name="index"),
]
