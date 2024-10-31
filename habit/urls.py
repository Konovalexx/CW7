from django.urls import path, include  # Не забудьте добавить include
from .views import (
    UserRegistrationView,
    WontListCreateView,
    PublicWontListView,
    WontDetailView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", include("rest_framework.urls")),  # Встроенные URL для аутентификации
    path("my-habits/", WontListCreateView.as_view(), name="my-habits"),
    path("public-habits/", PublicWontListView.as_view(), name="public-habits"),
    path("habits/<int:pk>/", WontDetailView.as_view(), name="habit-detail"),
]
