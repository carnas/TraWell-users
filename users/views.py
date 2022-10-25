from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from .serializers import UserSerializer
from users.models import User


class UserView(APIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params['id']
            user = User.objects.get(user_id=id)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={id} not found', safe=False)

        serializer = UserSerializer(user)

        return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)

    @classmethod
    def get_extra_actions(cls):
        return []
