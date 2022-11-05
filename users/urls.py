from django.urls import path

from .views import check_user, get_me, get_user

urlpatterns = [
    path('<int:user_id>', get_user),
    path('check_user', check_user),
    path('me', get_me)
]

