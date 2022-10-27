from django.urls import include, path

from rest_framework import routers

from . import api, views

router = routers.DefaultRouter()
router.register(r"rates", api.RateViewSet, basename="get_rates")

urlpatterns = [path("api/", include(router.urls))]

urlpatterns += [path("", views.index, name="index")]
