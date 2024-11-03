from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Wont
from .serializers import WontSerializer
from .permissions import IsOwner
from .pagination import CustomPagination


class BasePermissionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Задаем разрешения по умолчанию


# Список привычек текущего пользователя с пагинацией
class WontListCreateView(BasePermissionView, generics.ListCreateAPIView):
    serializer_class = WontSerializer
    pagination_class = CustomPagination  # Указываем класс пагинации

    def get_queryset(self):
        return Wont.objects.filter(user=self.request.user)


# Список публичных привычек с пагинацией
class PublicWontListView(BasePermissionView, generics.ListAPIView):
    queryset = Wont.objects.filter(is_published=True)
    serializer_class = WontSerializer
    pagination_class = CustomPagination  # Указываем класс пагинации


# Редактирование и удаление привычки
class WontDetailView(BasePermissionView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Wont.objects.all()
    serializer_class = WontSerializer
    permission_classes = [IsOwner]  # Только владелец и аутентифицированные пользователи