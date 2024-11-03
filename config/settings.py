import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv  # Импортируем для работы с переменными окружения

# Загрузка переменных окружения из .env файла
load_dotenv()

# CORS настройки
CORS_ALLOW_ALL_ORIGINS = False  # Убедитесь, что это значение соответствует вашим требованиям
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Укажите адрес вашего фронтенда
    "https://your-frontend-domain.com",  # Замените на ваш домен
]

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key_here")

DEBUG = True

ALLOWED_HOSTS = []  # Укажите разрешенные хосты для вашего приложения

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "habit",  # Приложение привычек
    "users",  # Приложение пользователей
    "django_celery_beat",  # Для Celery
    "corsheaders",  # Добавьте CORS заголовки
    "rest_framework",  # Добавьте Django REST Framework
    "drf_yasg",  # Добавьте drf_yasg для документации API
    "rest_framework_simplejwt",  # JWT
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Добавьте CORS Middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "drf2"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "12345"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"

AUTH_USER_MODEL = "users.User"  # Указываем модель пользователя

# Настройки Django REST Framework с Simple JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",  # Указываем класс пагинации по умолчанию
    "PAGE_SIZE": 10,  # Размер страницы
}

# Simple JWT настройки
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Celery Configuration
TG_API_KEY = os.environ.get("TG_API_KEY", "ваш_ключ_телеграмм")

# Убедитесь, что вы используете правильный URL брокера
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Укажите URL вашего брокера
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"  # Установите свой часовой пояс

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}