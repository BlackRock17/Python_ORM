from django.core.exceptions import ValidationError


def rating_validator(rating):
    if rating < 0 or rating > 10:
        raise ValidationError("The rating must be between 0.0 and 10.0")


def year_validator(year):
    if year < 1990 or year > 2023:
        raise ValidationError('The release year must be between 1990 and 2023')
