from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VehicleWithoutUserSerializer
from users.models import User
from vehicles.models import Vehicle
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from utils.authorization import is_authorized
from utils import users_utils
import jwt
import os


@api_view(['GET', 'POST'])
def user_vehicles(request, user_id):
    if is_authorized(request):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)

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


@api_view(['DELETE'])
def vehicle_details(request, car_id):
    if is_authorized(request):
        token = request.headers['Authorization'].split(' ')[1]
        try:
            public_key = f"""-----BEGIN RSA PUBLIC KEY-----\n{os.environ.get("TOKEN_KEY")}\n-----END RSA PUBLIC KEY-----"""
            issuer_claim = os.environ.get("ISSUER_CLAIM")
            email = jwt.decode(token, public_key, algorithms=['RS256'], issuer=issuer_claim,
                               audience='account', options={'verify_signature': True,
                                                            'verify_exp': True,
                                                            'verify_iss': True,
                                                            'verify_iat': True,
                                                            'verify_aud': True})['email']
            user = User.objects.get(email=email)
            vehicle = Vehicle.objects.get(vehicle_id=car_id)
            does_belong_to_user = vehicle.user.user_id == user.user_id
            if does_belong_to_user:
                vehicle.delete()
                return JsonResponse(status=status.HTTP_200_OK, data=f'Car with id={car_id} deleted succesfully',
                                    safe=False)
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

