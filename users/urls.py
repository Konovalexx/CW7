from django.urls import path
from .views import UserRegistrationView, UserDetailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('profile/', UserDetailView.as_view(), name='user_profile'),
]