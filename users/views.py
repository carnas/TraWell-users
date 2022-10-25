from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from users.models import User


class UserView(APIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get(self, request, *args, **kwargs):
        id = request.query_params['id']
        user = User.objects.get(user_id=id)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    @classmethod
    def get_extra_actions(cls):
        return []
