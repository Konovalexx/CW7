from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwner  # Импортируйте класс прав доступа


# Регистрация и получение списка пользователей
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Пользователь должен быть аутентифицирован для доступа к списку пользователей


# Получение, обновление и удаление информации о пользователе
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsOwner
    ]  # Только владелец может обновлять или удалять свои данные
