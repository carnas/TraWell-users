from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import VehicleWithoutUserSerializer
from users.models import User
from vehicles.models import Vehicle
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status


class VehicleView(APIView):
    serializer = VehicleWithoutUserSerializer

    @api_view(['GET'])
    def user_vehicles(request):
        if request.method == 'GET':
            user_id = request.query_params['user_id']
            try:
                user = User.objects.get(user_id=user_id)
                vehicles = Vehicle.objects.filter(user=user)
                serializer = VehicleWithoutUserSerializer(vehicles, many=True)

                return JsonResponse(status=status.HTTP_200_OK, data=serializer.data, safe=False)
            except User.DoesNotExist:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND, data=f'User with id={user_id} not found', safe=False)

