import os

import jwt
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from users.models import User
from utils import users_utils
from utils.authorization import is_authorized

from vehicles.models import Vehicle

from .serializers import VehicleWithoutUserSerializer


@api_view(['GET', 'POST'])
def user_vehicles(request, user_id):
    if is_authorized(request):
        try:
            user = User.objects.get(user_id=user_id)
            email = users_utils.decode_token(token)['email']
            if user.email != email:
                return JsonResponse(status=HTTP_403_FORBIDDEN, data=f'Not allowed', safe=False)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)
        except KeyError:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data='Something went wrong with user', safe=False)

        if request.method == 'GET':
            vehicles = Vehicle.objects.filter(user=user)
            serializer = VehicleWithoutUserSerializer(vehicles, many=True)
            return JsonResponse(status=status.HTTP_200_OK, data=serializer.data, safe=False)

        elif request.method == 'POST':
            vehicle_data = {key: value for key, value in request.data.items() if key in ['model', 'make', 'color']}

            try:
                vehicle = Vehicle.objects.create(make=vehicle_data['make'], model=vehicle_data['model'],
                                                 color=vehicle_data['color'], user=user)
                vehicle.save()
                serializer = VehicleWithoutUserSerializer(vehicle)
                return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
            except KeyError:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
            except ValidationError:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)


@api_view(['DELETE', 'PATCH'])
def vehicle_details(request, car_id):
    if is_authorized(request):
        token = request.headers['Authorization'].split(' ')[1]
        try:
            email = users_utils.decode_token(token)['email']
            user = User.objects.get(email=email)
            vehicle = Vehicle.objects.get(vehicle_id=car_id)
            does_belong_to_user = vehicle.user.user_id == user.user_id
            if does_belong_to_user:
                if request.method == 'DELETE':
                    vehicle.delete()
                    return JsonResponse(status=status.HTTP_200_OK, data=f'Car with id={car_id} deleted successfully',
                                        safe=False)
                elif request.method == 'PATCH':
                    serializer = VehicleWithoutUserSerializer(vehicle, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
                    else:
                        return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data="Wrong parameters", safe=False)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                                    data=f'Vehicle with id={car_id} does not belong to user with id={user.user_id}',
                                    safe=False)
        except KeyError:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data='Something went wrong with user', safe=False)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User not found', safe=False)
        except Vehicle.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'Car with id={car_id} not found', safe=False)
    else:
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data='Not authorized', safe=False)

