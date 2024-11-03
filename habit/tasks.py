import json
import logging
from datetime import datetime

import requests
from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import TG_API_KEY
from .models import Wont

logger = logging.getLogger(__name__)

@shared_task
def create_periodic_tasks():
    try:
        response = requests.get(f"https://api.telegram.org/bot{TG_API_KEY}/getupdates")
        response.raise_for_status()  # Проверка на успешный ответ
        data = response.json()

        if not data.get("result"):
            logger.warning("Бот не активен или нет обновлений.")
            return

        last_update = data["result"][-1]
        message = last_update.get("message")

        # Проверка на наличие сообщения и извлечение username и chat_id
        if message is None:
            logger.warning("Нет сообщения в обновлении.")
            return

        username = message["chat"].get("username")
        chat_id = message["chat"]["id"]

        if username is None:
            logger.warning("Нет имени пользователя для чата.")
            return

        wonts = Wont.objects.filter(user__username=username)
        for wont in wonts:
            # Определение частоты отправки
            every = 1 if wont.period == "daily" else 7 if "weekly" in wont.period else 30
            task_name = f"Send message ({username}) ({wont.pk})"

            # Проверяем, существует ли уже задача
            if not PeriodicTask.objects.filter(name=task_name).exists():
                logger.info("Добавление задачи: %s", task_name)
                schedule, _ = IntervalSchedule.objects.get_or_create(
                    every=every,
                    period=IntervalSchedule.DAYS,
                )

                text = f"Я буду {wont.action} в {wont.time} в {wont.place}"
                start_time = datetime.now().replace(hour=wont.time.hour, minute=wont.time.minute)

                PeriodicTask.objects.create(
                    interval=schedule,
                    name=task_name,
                    task="habit.tasks.send_message",
                    args=json.dumps([text, chat_id]),  # Используйте chat_id здесь
                    start_time=start_time,
                )
            else:
                logger.info("Задача уже существует: %s", task_name)

    except requests.RequestException as e:
        logger.error("Ошибка при запросе к Telegram API: %s", e)
    except Exception as e:
        logger.error("Ошибка при создании периодических задач: %s", e)

@shared_task
def send_message(text, chat_id):
    try:
        params = {"chat_id": chat_id, "text": text}
        response = requests.get(f"https://api.telegram.org/bot{TG_API_KEY}/sendMessage", params=params)
        response.raise_for_status()  # Проверка на успешный ответ
        logger.info("Сообщение отправлено: %s", text)
    except requests.HTTPError as e:
        logger.error("Ошибка при отправке сообщения в Telegram: %s", e.response.json())
        error_message = e.response.json().get("description", "Неизвестная ошибка")
        return f"Ошибка отправки сообщения: {error_message}"  # Возвращаем более информативное сообщение об ошибке
    except requests.RequestException as e:
        logger.error("Ошибка при отправке сообщения в Telegram: %s", e)
        return "Ошибка соединения с Telegram. Пожалуйста, попробуйте позже."
    except Exception as e:
        logger.error("Ошибка при обработке сообщения: %s", e)
        return "Произошла ошибка при обработке сообщения."