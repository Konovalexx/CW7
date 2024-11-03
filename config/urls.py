from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка схемы документации
schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version="v1",
        description="API documentation for your project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Маршруты для приложения habits
    path("api/habits/", include("habit.urls")),

    # Маршруты для приложения users
    path("api/users/", include("users.urls")),

    # JWT-токены для аутентификации
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger UI для документации
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # ReDoc для альтернативной документации
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]