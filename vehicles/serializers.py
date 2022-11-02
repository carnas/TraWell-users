from rest_framework import serializers

from vehicles.models import Vehicle
from users.models import User


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'user_type', 'facebook', 'instagram',
                  'avatar')


class VehicleSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(many=False)

    class Meta:
        model = Vehicle
        fields = ('vehicle_id', 'make', 'model', 'color', 'user')


class VehicleWithoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('vehicle_id', 'make', 'model', 'color')
