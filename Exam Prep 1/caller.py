import os
import django
from django.db.models import Q, Count, Avg, F

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

def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('movie')
                                    ).order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if top_movie is None:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'

    participated_actors = top_movie.actors.all().order_by('full_name')

    cast = ', '.join(actor.full_name for actor in participated_actors)

    return (f"Top rated awarded movie: {top_movie.title},"
            f" rating: {top_movie.rating:.1f}."
            f" Starring actor: {starring_actor}. Cast: {cast}.")


def increase_rating():
    num_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0).update(rating=F('rating') + 0.1)

    if num_movies == 0:
        return "No ratings increased."
    else:
        return f"Rating increased for {num_movies} movies."

