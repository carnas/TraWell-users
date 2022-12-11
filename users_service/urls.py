from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import users
from users import urls
import vehicles.views
import vehicles
from vehicles import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(users.urls)),
    path('vehicles/', include(vehicles.urls)),
]
