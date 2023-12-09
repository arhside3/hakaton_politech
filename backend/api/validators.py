import re
from django.core.exceptions import ValidationError

from backend.settings import RESERVED_USERNAME


def validate_bad_username(value):
    invalid_chars = re.findall(r'[^\w.@+-]', value)

    if invalid_chars:
        raise ValidationError(
            f"Имя пользователя содержит недопустимые символы: "
            f"{''.join(set(invalid_chars))}"
        )

    return value


def validate_username(value):
    if value == RESERVED_USERNAME:
        raise ValidationError(f'Нельзя сделать ник с таким значением: {value}')

    return value
