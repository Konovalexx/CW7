import json
import requests
from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from config.settings import TG_API_KEY
from .models import Wont
from datetime import datetime


@shared_task
def create_periodic_tasks():
    data = requests.get(f"https://api.telegram.org/bot{TG_API_KEY}/getupdates").json()
    if data and "result" in data:
        username = data["result"][-1]["message"]["chat"]["username"]
    else:
        print("Бот не активен")
        return

    wonts = Wont.objects.filter(
        user__username=username
    )  # Исправление на user__username
    for wont in wonts:
        if wont.period == "daily":
            every = 1
        elif "weekly" in wont.period:  # Проверка на еженедельные привычки
            every = 7
        else:
            every = 30

        if not PeriodicTask.objects.filter(
            name=f"Send message ({username}) ({wont.pk})"
        ).exists():
            print("Задача добавлена")
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=every,
                period=IntervalSchedule.DAYS,
            )
            text = f"Я буду {wont.action} в {wont.time} в {wont.place}"
            PeriodicTask.objects.create(
                interval=schedule,
                name=f"Send message ({username}) ({wont.pk})",
                task="habit.tasks.send_message",
                args=json.dumps([text, data["result"][-1]["message"]["chat"]["id"]]),
                start_time=str(datetime.now())
                + str(wont.time.hour)
                + str(wont.time.minute),
            )


@shared_task
def send_message(text, chat_id):
    params = {"chat_id": chat_id, "text": text}
    requests.get(
        f"https://api.telegram.org/bot{TG_API_KEY}/sendMessage", params=params
    ).json()
