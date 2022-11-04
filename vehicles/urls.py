from django.urls import path
from .views import user_vehicles, vehicle_details

urlpatterns = [
    path('user_vehicles/<int:user_id>', user_vehicles),
    path('<int:car_id>', vehicle_details),
]
