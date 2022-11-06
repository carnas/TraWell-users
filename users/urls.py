from django.urls import path

from .views import check_user, get_me, user_details 

urlpatterns = [
    path('<int:user_id>', user_details),
    path('check_user', check_user),
    path('me', get_me)
]

