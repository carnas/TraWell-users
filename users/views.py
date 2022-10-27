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

    @api_view(['POST'])
    def check_user(self, request):
        encoded_jwt = request.query_params['data']
        user_data = utils.get_user_data_from_jwt(encoded_jwt)
        email = user_data['email']
        if utils.is_email_valid(email):
            try:
                user_with_email = User.objects.get(email=email)
                serializer = UserSerializer(user_with_email, data=user_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    serializer = self.get_serializer(user_with_email)
                    return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
                else:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
            except User.DoesNotExist:
                new_user = User.objects.create(first_name=user_data['first_name'], last_name=user_data['last_name'],
                                               email=user_data['email'], date_of_birth=user_data['date_of_birth'],
                                               user_type=user_data['user_type'], facebook=user_data['facebook'],
                                               instagram=user_data['instagram'], avatar=user_data['avatar'])

                new_user.save()
                serializer = UserSerializer(new_user)

                return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=f"Email: {email} is not valid", safe=False)

    @classmethod
    def get_extra_actions(cls):
        return []
