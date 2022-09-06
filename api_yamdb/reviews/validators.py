from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Функции проверки корректности года создания произведения."""

    if value > dt.now().year:
        raise ValidationError(
            "Указанный год еще не наступил! Проверьте введенные данные!")
