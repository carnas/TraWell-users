from django.urls import path
from .views import UserView

urlpatterns = [
    path('', UserView.as_view()),
    path('check_user', UserView.check_user),
]

