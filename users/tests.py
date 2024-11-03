from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class UserTests(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя для использования в тестах
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.chat_id = '12345'
        self.user.save()
        self.url_register = reverse('user_register')
        self.url_profile = reverse('user_profile')

    def test_user_registration(self):
        # Тест регистрации нового пользователя
        data = {
            "username": "newuser",
            "password": "newpassword",
            "chat_id": "54321"
        }
        response = self.client.post(self.url_register, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Проверка, что увеличилось количество пользователей
        self.assertEqual(User.objects.get(username='newuser').chat_id, '54321')  # Проверка chat_id

    def test_user_registration_password_min_length(self):
        # Тест на короткий пароль
        data = {
            "username": "newuser",
            "password": "short",
            "chat_id": "54321"
        }
        response = self.client.post(self.url_register, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Проверка наличия ошибки по паролю

    def test_user_profile(self):
        # Тест получения профиля текущего пользователя
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')  # Проверка имени пользователя

    def test_user_profile_update(self):
        # Тест обновления информации о пользователе
        self.client.login(username='testuser', password='testpassword')
        data = {
            "username": "updateduser",  # Обновите имя пользователя
            "password": "newpassword",  # Можно обновить пароль
            "chat_id": "updated_chat_id"  # Обновление chat_id
        }
        response = self.client.put(self.url_profile, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Обновление информации о пользователе
        self.assertEqual(self.user.username, 'updateduser')  # Проверка обновленного имени пользователя
        self.assertEqual(self.user.chat_id, 'updated_chat_id')  # Проверка обновленного chat_id

    def test_user_profile_update_password(self):
        # Тест обновления пароля пользователя
        self.client.login(username='testuser', password='testpassword')
        data = {
            "username": "testuser",
            "password": "newpassword"
        }
        response = self.client.put(self.url_profile, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Обновление информации о пользователе
        self.assertTrue(self.user.check_password("newpassword"))  # Проверка нового пароля

    def test_user_profile_delete(self):
        # Тест удаления профиля пользователя
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(self.url_profile)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Проверка, что пользователь удален