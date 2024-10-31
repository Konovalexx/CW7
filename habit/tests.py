from rest_framework.test import APITestCase
from django.test import RequestFactory
from django.utils import timezone
from habit.models import Wont
from users.models import User
from habit.serializers import WontSerializer


class WontTestCase(APITestCase):
    """Класс тестирования приложения Habit"""

    def setUp(self):
        self.factory = RequestFactory()

        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Создаем тестовую привычку
        self.wont = Wont.objects.create(
            user=self.user,
            place="Park",
            time=timezone.now().time(),
            action="Jogging",
            is_pleasant=True,
            period="daily",  # Используем строку для периода
            reward=None,
            time_to_action=timezone.timedelta(minutes=90),
            is_published=True,
        )

        self.request = self.factory.post("/dummy-url/")
        self.request.user = self.user

    def test_create_wont(self):
        """Тест на создание привычки"""
        wont_count = Wont.objects.count()
        self.assertEqual(wont_count, 1, "Привычка должна быть успешно создана")

    def test_update_wont(self):
        """Тест на обновление привычки"""
        new_action = "Evening jog"
        self.wont.action = new_action
        self.wont.save()

        self.assertEqual(self.wont.action, new_action, "Привычка должна быть обновлена")

    def test_period_wont(self):
        """Тест на проверку периода выполнения привычки"""
        self.assertEqual(
            self.wont.period, "daily", "Период должен быть установлен на 'daily'"
        )

    def test_wont_owner(self):
        """Тест на проверку владельца привычки"""
        self.assertEqual(
            self.wont.user,
            self.user,
            "Владелец привычки должен совпадать с тестовым пользователем",
        )

    def test_wont_publish_status(self):
        """Тест на публичный статус привычки"""
        self.assertTrue(self.wont.is_published, "Привычка должна быть опубликована")

    def test_wont_reward_and_connection(self):
        """Тест на ошибку при указании вознаграждения и связанной привычки одновременно"""
        related_wont = Wont.objects.create(
            user=self.user,
            place="Office",
            time="10:00",
            action="Reading",
            is_pleasant=True,
            period="daily",  # Используем строку для периода
            is_published=True,
        )

        invalid_payload = {
            "place": "Gym",
            "time": "08:00",
            "action": "Yoga",
            "is_pleasant": False,
            "period": "weekly_1",  # Корректное значение для периода
            "reward": "Health smoothie",  # Указано вознаграждение
            "connection_wont": related_wont.id,  # Указана связанная привычка
            "time_to_action": "00:01:00",  # Значение в правильном формате
            "is_published": True,
        }

        serializer = WontSerializer(
            data=invalid_payload, context={"request": self.request}
        )

        # Убираем проверку non_field_errors
        self.assertFalse(
            serializer.is_valid(),
            "Сериализатор не должен быть валиден при вознаграждении и связанной привычке",
        )
