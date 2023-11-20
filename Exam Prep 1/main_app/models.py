from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator

from main_app.managers import DirectorManager
from main_app.mixins import Person, Awarded, LastUpdated


class Director(Person):

    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )

    objects = DirectorManager()


class Actor(Person, Awarded, LastUpdated):
    ...


class Movie(Awarded, LastUpdated):

    class GENRE_CHOICES(models.TextChoices):
        Action = 'Action'
        Comedy = 'Comedy'
        Drama = 'Drama'
        Other = 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        blank=True,
        null=True
    )

    genre = models.CharField(
        max_length=6,
        default='Other',
        choices=GENRE_CHOICES.choices
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movies'
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='movies'
    )

    actors = models.ManyToManyField(
        to=Actor,
    )