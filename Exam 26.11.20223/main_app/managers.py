from django.db import models
from django.db.models import Count


class AuthorManager(models.Manager):

    def get_authors_by_article_count(self):
        author_by_num_articles = self.annotate(
            num_article=Count('article')
        ).order_by(
            '-num_article', 'email',
        )

        return author_by_num_articles
