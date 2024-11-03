from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwner


# Регистрация пользователя
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Открытая регистрация


# Получение, обновление и удаление информации о пользователе
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner
    ]  # Только владелец может обновлять или удалять свои данные

    def get_object(self):
        # Возвращает текущего пользователя
        return self.request.user