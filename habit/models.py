from django.db import models
from django.utils import timezone
from users.models import User  # Импортируем модель пользователя


class Wont(models.Model):
    CHOICES_PERIOD = (
        ("daily", "Ежедневная"),
        ("weekly_1", "1 раз в неделю"),
        ("weekly_2", "2 раза в неделю"),
        ("weekly_3", "3 раза в неделю"),
        ("weekly_4", "4 раза в неделю"),
        ("weekly_5", "5 раз в неделю"),
        ("weekly_6", "6 раз в неделю"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="Создатель"
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=100, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=True, verbose_name="Признак приятной привычки"
    )
    connection_wont = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, verbose_name="Связанная привычка"
    )
    period = models.CharField(
        max_length=20, default="daily", choices=CHOICES_PERIOD, verbose_name="Период"
    )  # Выбор периода
    reward = models.CharField(max_length=100, null=True, verbose_name="Вознаграждение")
    time_to_action = models.DurationField(
        default=timezone.timedelta(seconds=60), verbose_name="Время на выполнение"
    )  # Время на выполнение
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    def save(self, *args, **kwargs):
        if not self.time:  # Проверяем, если time еще не установлен
            self.time = (
                timezone.now() + timezone.timedelta(minutes=3)
            ).time()  # Устанавливаем значение по умолчанию
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} в {self.place} в {self.time}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
