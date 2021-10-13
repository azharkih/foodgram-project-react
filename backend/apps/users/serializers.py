from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User

from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class RegistrationUserSerializer(serializers.ModelSerializer):
    """ Класс UserSerializer описывает сериализатор данных запроса на основе
    модели User.

    Родительский класс -- serializers.ModelSerializer.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'password', 'username',
                  'email')
        model = User

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     new_password = serializers.CharField(write_only=True, required=True)
#     current_password = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('new_password', 'current_password')
#
#     def validate_current_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError(
#                 {'current_password': 'Current password is not correct'})
#         return value
#
#     def update(self, instance, validated_data):
#         instance.set_password(validated_data['password'])
#         instance.save()
#         return instance
