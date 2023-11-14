import re

from django.core.exceptions import ValidationError


def validate_name(name):
    for char in name:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError("Name can only contain letters and spaces")


def phone_validator(phone):
    if not re.match(r"\+359\d{9}$", phone):
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")