from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


class UserSer(serializers.ModelSerializer):
    # Сериализация пользователя
    class Meta:
        model = User
        fields = ("username", "email",)


class ProfileSer(serializers.ModelSerializer):
    """Для вывода профиля пользователя"""
    user = UserSer()

    class Meta:
        model = Profile
        fields = (
            "user",
            "nike",
            "avatar",
            "email_two",
            "phone",
            "first_name",
            "last_name"
        )


class ProfileUpdateSer(serializers.ModelSerializer):
    """Редактирование профиля пользователя"""

    class Meta:
        model = Profile
        fields = (
            "nike",
            "avatar",
            "email_two",
            "phone",
            "first_name",
            "last_name"
        )


