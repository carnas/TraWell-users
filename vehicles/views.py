from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VehicleWithoutUserSerializer
from users.models import User
from vehicles.models import Vehicle
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status


@api_view(['GET', 'POST'])
def user_vehicles(request, user_id):
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

