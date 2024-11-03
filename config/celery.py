from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Укажите стандартный Django настройки модуля
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('CW7')  # Замените 'CW7' на имя вашего проекта

# Загрузите настройки Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически найдите задачи в установленных приложениях
app.autodiscover_tasks()

# Настройка периодических задач (если необходимо)
app.conf.beat_schedule = {
    'send_message_task': {  # Уникальное имя для задачи
        'task': 'habit.tasks.send_message',  # Укажите путь к вашей задаче
        'schedule': 60.0,  # Период выполнения задачи в секундах
    },
}