from rest_framework import serializers
from .models import User, Wont
from .validators import (
    validate_wont_and_reward,
    validate_linked_wont,
    validate_pleasant_wont,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "chat_id"]
        ref_name = "HabitUserSerializer"


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
        # Проверяем, что значение period соответствует одному из вариантов
        valid_periods = dict(self.Meta.model.CHOICES_PERIOD).keys()
        if value not in valid_periods:
            raise serializers.ValidationError(
                "Период выполнения должен быть одним из следующих: "
                + ", ".join(valid_periods)
            )
        return value  # Возвращаем проверенное значение

    def validate_time_to_action(self, value):
        # Проверяем, что значение time_to_action является числом
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError(
                "Время на выполнение должно быть числом (в секундах)."
            )

        # Валидация времени выполнения привычки
        if value > 120:
            raise serializers.ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд."
            )

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
