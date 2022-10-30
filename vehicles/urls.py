from django.urls import path
from .views import user_vehicles

urlpatterns = [
    path('user_vehicles/<int:user_id>', user_vehicles),
]
