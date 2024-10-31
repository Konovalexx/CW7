from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    chat_id = models.CharField(
        max_length=255, verbose_name="chat_id", null=True, blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
