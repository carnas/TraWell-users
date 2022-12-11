from rest_framework import serializers

from users.models import User


class UserToUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'facebook', 'instagram', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'avg_rate', 'user_type', 'facebook',
                  'instagram', 'avatar')
