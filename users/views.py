from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from users.models import User
from users_service.celery import queue_rides, queue_notify, queue_reviews
from utils import users_utils
from utils.authorization import is_authorized
from users_service import tasks
from .serializers import UserSerializer, UserToUpdateSerializer


@api_view(['GET', 'PATCH'])
def user_details(request, user_id):
    if is_authorized(request):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
        
        elif request.method == 'PATCH':
            token = request.headers['Authorization'].split(' ')[1]
            try:
                email = users_utils.decode_token(token)['email']
                want_to_change_sb_else_data = user.email != email
                if want_to_change_sb_else_data:
                    return JsonResponse(status=status.HTTP_403_FORBIDDEN,
                                        data='No permission to change data of another person', safe=False)
                else:
                    serializer = UserToUpdateSerializer(user, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        serializer = UserSerializer(user)

                        tasks.publish_message(serializer.data, 'users', queue_rides, 'send')
                        tasks.publish_message(serializer.data, 'users', queue_notify, 'notify')
                        tasks.publish_message(serializer.data, 'users', queue_reviews, 'review')

                        return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
                    else:
                        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
            except KeyError:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data='Invalid token', safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)


@api_view(['GET'])
def check_user(request):
    if is_authorized(request):
        token = request.headers['Authorization'].split(' ')[1]
        user_data = users_utils.get_user_data_from_token(token)
        if 'error' not in user_data.keys():
            email = user_data['email']
            try:
                user = User.objects.get(email=email)

                tasks.publish_message(UserSerializer(user).data, 'users', queue_notify, 'notify')
                tasks.publish_message(UserSerializer(user).data, 'users', queue_rides, 'send')
                tasks.publish_message(UserSerializer(user).data, 'users', queue_reviews, 'review')

                return JsonResponse(status=status.HTTP_200_OK, data='User in database', safe=False)
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
                    tasks.publish_message(serializer.data, 'users', queue_notify, 'notify')
                    tasks.publish_message(serializer.data, 'users', queue_rides, 'send')
                    tasks.publish_message(serializer.data, 'users', queue_reviews, 'review')

                    return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
                except ValidationError:
                    return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=user_data['error'], safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)


@api_view(['GET'])
def get_me(request):
    if is_authorized(request):
        token = request.headers['Authorization'].split(' ')[1]
        user_data = users_utils.get_user_data_from_token(token)
        if 'error' not in user_data.keys():
            email = user_data['email']
            try:
                user = User.objects.get(email=email)
                return JsonResponse(status=status.HTTP_200_OK, data={'user_id': user.user_id})
            except User.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User not found', safe=False)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data=user_data['error'], safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)
