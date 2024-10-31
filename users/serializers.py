from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "chat_id"]
        ref_name = (
            "UsersUserSerializer"  # Уникальное имя для сериализатора в приложении users
        )
