from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.decorators import api_view

from . import tasks
from .serializers import UserSerializer
from users.models import User
from utils.authorization import is_authorized
from django.core.exceptions import ValidationError

from utils import users_utils


@api_view(['GET'])
def get_user(request, user_id):
    authorized = is_authorized(request)
    if authorized:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)

        serializer = UserSerializer(user)

        return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)


@api_view(['GET'])
def check_user(request):
    authorized = is_authorized(request)
    print(authorized)
    if authorized:
        token = request.headers['Authorization']
        user_data = users_utils.get_user_data_from_token(token)
        if 'error' not in user_data.keys():
            email = user_data['email']
            if users_utils.is_email_valid(email):
                try:
                    user_with_email = User.objects.get(email=email)
                    # Get data that can be updated
                    user_data = {'first_name': user_data['first_name'],
                                 'last_name': user_data["last_name"],
                                 'date_of_birth': user_data['date_of_birth'],
                                 'facebook': user_data['facebook'],
                                 'instagram': user_data['instagram'],
                                 'avatar': user_data['avatar']
                                 }
                    serializer = UserSerializer(user_with_email, data=user_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()

                        tasks.publish_message(serializer.data)
                        tasks.publish_message_n(serializer.data)

                        return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
                    else:
                        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
                except User.DoesNotExist:
                    try:
                        new_user = User.objects.create(first_name=user_data['first_name'],
                                                       last_name=user_data['last_name'],
                                                       email=user_data['email'],
                                                       date_of_birth=user_data['date_of_birth'],
                                                       user_type=user_data['user_type'], facebook=user_data['facebook'],
                                                       instagram=user_data['instagram'], avatar=user_data['avatar'])
                        new_user.save()
                        serializer = UserSerializer(new_user)

                        tasks.publish_message(serializer.data)
                        tasks.publish_message_n(serializer.data)

                        return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
                    except ValidationError:
                        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=f"Email: {email} is not valid", safe=False)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=user_data['error'], safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)
