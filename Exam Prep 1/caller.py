import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Director

# Create and run your queries within functions


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    if search_name and search_nationality:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    else:
        return ''

    directors = Director.objects.filter(query).order_by('full_name')

    result = []

    for director in directors:
        result.append(
                      f'Director: {director.full_name},'
                      f' nationality: {director.nationality},'
                      f' experience: {director.years_of_experience}'
        )

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count(
    ).annotate(num_of_movies=Count('movies')
               ).order_by('-num_of_movies', 'full_name'
                          ).first()

    return f"Top Director: {director.full_name}, movies: {director.num_of_movies}."


