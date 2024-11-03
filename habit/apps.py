from django.apps import AppConfig
from django.db.models.signals import post_migrate

class HabitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "habit"

    def ready(self):
        # Импортируйте вашу задачу только когда приложение готово
        from .tasks import create_periodic_tasks  # Импорт здесь

        # Подключаем сигнал, который вызовет create_periodic_tasks после миграции
        post_migrate.connect(self.create_periodic_tasks_on_migrate, sender=self)

    def create_periodic_tasks_on_migrate(self, sender, **kwargs):
        from .tasks import create_periodic_tasks  # Импортируем задачу снова
        create_periodic_tasks.delay()  # Вызываем задачу асинхронно