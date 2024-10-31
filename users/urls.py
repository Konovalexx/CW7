from django.urls import path
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    path(
        "", UserListCreateView.as_view(), name="user-list-create"
    ),  # Список пользователей и создание нового пользователя
    path(
        "<int:pk>/", UserDetailView.as_view(), name="user-detail"
    ),  # Получение, обновление и удаление пользователя
]
