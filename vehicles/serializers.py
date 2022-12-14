from rest_framework import serializers
from users.models import User

from vehicles.models import Vehicle


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'avg_rate', 'user_type',
                  'facebook', 'instagram', 'avatar')


class VehicleSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(many=False)

    class Meta:
        model = Vehicle
        fields = ('vehicle_id', 'make', 'model', 'color', 'user')


class VehicleWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('vehicle_id', 'make', 'model', 'color')
