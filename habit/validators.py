from django.core.exceptions import ValidationError


# Валидатор, запрещающий одновременный выбор связанной привычки и вознаграждения
def validate_wont_and_reward(wont, reward):
    if wont and reward:
        raise ValidationError("Одновременный выбор вознаграждения и связанной привычки")


# Валидатор, проверяющий время выполнения привычки (в секундах)
def validate_time(time_seconds):
    if time_seconds and time_seconds > 120:
        raise ValidationError(
            "Время выполнения привычки не должно превышать 120 секунд"
        )


# Валидатор, проверяющий, что связанная привычка приятная
def validate_linked_wont(wont):
    if wont and not wont.is_pleasant:
        raise ValidationError(
            "Связанные привычки могут быть только с признаком приятной привычки."
        )


# Валидатор, проверяющий, что у приятной привычки нет вознаграждения или связанной привычки
def validate_pleasant_wont(is_pleasant, wont, reward):
    if is_pleasant and (wont or reward):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


# Валидатор, проверяющий период выполнения привычки
def validate_period(period):
    try:
        period = int(period)  # Преобразуем period в целое число
    except ValueError:
        raise ValidationError("Период выполнения должен быть числом.")

    if not 1 <= period <= 7:
        raise ValidationError(
            "Нельзя выполнять привычку реже чем 1 раз в неделю или чаще 7 раз в неделю."
        )
