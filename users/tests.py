from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User


class UserTests(APITestCase):
    """Тестирование приложения пользователей"""

    def setUp(self):
        """Создаем тестового пользователя"""
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", chat_id="123456"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_create_user(self):
        """Тест на создание пользователя"""
        url = reverse("user-list-create")
        data = {"username": "newuser", "password": "newpassword", "chat_id": "654321"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username="newuser").chat_id, "654321")

    def test_list_users(self):
        """Тест на получение списка пользователей"""
        url = reverse("user-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Должен вернуть 1 пользователя

    def test_retrieve_user(self):
        """Тест на получение информации о пользователе"""
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_update_user(self):
        """Тест на обновление информации о пользователе"""
        url = reverse("user-detail", args=[self.user.id])
        data = {"username": "updateduser", "chat_id": "987654"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.chat_id, "987654")

    def test_delete_user(self):
        """Тест на удаление пользователя"""
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)  # Пользователь должен быть удален
