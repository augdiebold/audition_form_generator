from django.core.exceptions import ValidationError


def validate_name(value):
    if not value.isalpha():
        raise ValidationError('Field "name" only accept letters')