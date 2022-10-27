from django.urls import include, path

from rest_framework import routers

from . import api, views

router = routers.DefaultRouter()
router.register(r"rates", api.RateViewSet, basename="get_rates")

urlpatterns = [path("", views.index, name="index"), path("api/", include(router.urls))]
