from django.urls import path
from .views import VehicleView

urlpatterns = [
    path('user_vehicles/', VehicleView.user_vehicles),
]
