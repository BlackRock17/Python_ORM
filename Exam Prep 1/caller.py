import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Director, Actor, Movie


# Create and run your queries within functions


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    if search_name and search_nationality:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    else:
        query = Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []

    for director in directors:
        result.append(
                      f'Director: {director.full_name},'
                      f' nationality: {director.nationality},'
                      f' experience: {director.years_of_experience}'
        )

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.num_movies}."


def get_top_actor():
    actor = Actor.objects.annotate(starred_in=Count('movies')
                                   ).order_by('-starred_in', 'full_name').first()

    actor_movies = Movie.objects.filter(starring_actor=actor)

    if not actor or not actor_movies:
        return ''

    avg_rating = actor_movies.aggregate(avg_rating=Avg('rating'))['avg_rating']

    return (f"Top Actor: {actor.full_name}, starring in movies: {', '.join([movie.title for movie in actor_movies])}, "
            f"movies average rating: {avg_rating:.1f}")


# def get_top_actor():
#     actor = Actor.objects.prefetch_related('movies') \
#         .annotate(
#         num_of_movies=Count('movies'),
#         movies_avg_rating=Avg('movies__rating')) \
#         .order_by('-num_of_movies', 'full_name') \
#         .first()
#
#     if not actor or not actor.num_of_movies:
#         return ""
#
#     movies = ", ".join(movie.title for movie in actor.movies.all() if movie)
#
#     return f"Top Actor: {actor.full_name}, starring in movies: {movies}, " \
#            f"movies average rating: {actor.movies_avg_rating:.1f}"

