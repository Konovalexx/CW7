from django.contrib import admin
from .models import Wont


@admin.register(Wont)
class WontAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "place",
        "time",
        "user",
        "is_pleasant",
        "period",
        "is_published",
    )
