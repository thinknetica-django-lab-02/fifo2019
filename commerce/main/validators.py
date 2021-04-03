from datetime import date
from django.forms import ValidationError


def validator_age(value):
    """Проверка возраста - 18 лет"""

    today = date.today()
    if int(today.year - value.year) < 18:
        raise ValidationError('Возраст меньше 18 лет!')
    return value

