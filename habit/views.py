from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Wont
from .serializers import WontSerializer, UserSerializer
from .permissions import IsOwner
from django.contrib.auth import get_user_model

User = get_user_model()


# Регистрация пользователя
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Список привычек текущего пользователя с пагинацией
class WontListCreateView(generics.ListCreateAPIView):
    serializer_class = WontSerializer
    permission_classes = [IsAuthenticated]  # Пользователь должен быть аутентифицирован

    def get_queryset(self):
        return Wont.objects.filter(user=self.request.user)


# Список публичных привычек
class PublicWontListView(generics.ListAPIView):
    queryset = Wont.objects.filter(is_published=True)
    serializer_class = WontSerializer


# Редактирование и удаление привычки
class WontDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wont.objects.all()
    serializer_class = WontSerializer
    permission_classes = [
        IsOwner,
        IsAuthenticated,
    ]  # Только владелец и аутентифицированные пользователи
