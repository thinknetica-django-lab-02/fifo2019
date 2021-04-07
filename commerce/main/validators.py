from datetime import datetime, date
from django.forms import ValidationError


def validator_age(date_of_birth):
    """Проверка возраста - 18 лет"""

    today = datetime.now().date()
    date_limit = date(today.year - 18, today.month, today.day)
    diff = date_limit - date_of_birth

    if diff.days < 0:
        raise ValidationError('Возраст меньше 18 лет!')

    return date_of_birth

