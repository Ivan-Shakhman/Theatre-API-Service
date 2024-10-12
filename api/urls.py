from django.urls import include, path
from rest_framework import routers

from api import views

app_name = "api"

router = routers.DefaultRouter()
router.register("genres", views.GenreViewSet)
router.register("actors", views.ActorViewSet)
router.register("theatre-halls", views.TheatreHallViewSet)
router.register("plays", views.PlayViewSet)
router.register("performances", views.PerformanceViewSet)
router.register("reservations", views.ReservationViewSet)


urlpatterns = [path("", include(router.urls))]