import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Author, Article, Review


# Create and run your queries within functions


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = query_name & query_email
    elif search_name is not None:
        query = query_name
    elif search_email is not None:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ''

    result = []

    for author in authors:
        is_banned = 'Banned' if author.is_banned else 'Not Banned'
        result.append(f'Author: {author.full_name}, email: {author.email}, status: {is_banned}')

    return '\n'.join(result)


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()

    if author is not None and author.num_article > 0:
        return f'Top Author: {author.full_name} with {author.num_article} published articles.'
    return ''


def get_top_reviewer():
    author = Author.objects.annotate(
        num_reviews=Count('review')
    ).order_by(
        '-num_reviews', 'email',
    ).first()

    if author is not None and author.num_reviews > 0:
        return f'Top Reviewer: {author.full_name} with {author.num_reviews} published reviews.'
    return ''


def get_latest_article():
    article = Article.objects.order_by('-published_on').first()

    if article is not None and article.article_review.count() > 0:
        authors = [a.full_name for a in article.authors.all().order_by('full_name')]
        num_rating = article.article_review.count()
        avg_rating = article.article_review.aggregate(Avg('rating'))['rating__avg']

        return (f'The latest article is: {article.title}.'
                f' Authors: {", ".join(authors)}.'
                f' Reviewed: {num_rating} times.'
                f' Average Rating: {avg_rating:.2f}.')

    return ''


def get_top_rated_article():
    article = (
        Article.objects.annotate(avg_rating=Avg('article_review__rating'), num_reviews=Count('article_review'))
        .filter(article_review__isnull=False)
        .order_by('-avg_rating', 'title')
        .first()
    )

    if article and article.num_reviews > 0:
        formatted_avg_rating = "{:.2f}".format(article.avg_rating)
        return f"The top-rated article is: {article.title}, with an average rating of {formatted_avg_rating}, reviewed {article.num_reviews} times."
    else:
        return ""


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."

    num_reviews = Review.objects.filter(author=author).count()

    author.is_banned = True
    author.save()
    Review.objects.filter(author=author).delete()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
