from rest_framework import serializers
from users.serializers import UserSerializer  # Импорт из приложения users
from .models import Wont
from .validators import (
    validate_wont_and_reward,
    validate_linked_wont,
    validate_pleasant_wont,
    validate_period,
    validate_time,
)

class WontSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Wont
        fields = [
            "id",
            "action",
            "place",
            "time",
            "user",
            "is_pleasant",
            "period",
            "reward",
            "time_to_action",
            "is_published",
        ]
        read_only_fields = ["user"]

    def validate_period(self, value):
        validate_period(value)  # Используем валидатор
        return value  # Возвращаем проверенное значение

    def validate_time_to_action(self, value):
        # Проверяем, что значение time_to_action является числом
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError(
                "Время на выполнение должно быть числом (в секундах)."
            )
        validate_time(value)  # Используем валидатор
        return value  # Возвращаем проверенное значение

    def validate(self, attrs):
        # Проверяем связанные валидаторы
        validate_wont_and_reward(attrs.get("connection_wont"), attrs.get("reward"))
        validate_linked_wont(attrs.get("connection_wont"))
        validate_pleasant_wont(
            attrs.get("is_pleasant"), attrs.get("connection_wont"), attrs.get("reward")
        )

        return attrs

    def create(self, validated_data):
        # Установка текущего пользователя в валидационные данные
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Обновление данных привычки
        instance.action = validated_data.get("action", instance.action)
        instance.place = validated_data.get("place", instance.place)
        instance.time = validated_data.get("time", instance.time)
        instance.is_pleasant = validated_data.get("is_pleasant", instance.is_pleasant)
        instance.period = validated_data.get("period", instance.period)
        instance.reward = validated_data.get("reward", instance.reward)
        instance.time_to_action = validated_data.get(
            "time_to_action", instance.time_to_action
        )
        instance.is_published = validated_data.get(
            "is_published", instance.is_published
        )
        instance.save()
        return instance