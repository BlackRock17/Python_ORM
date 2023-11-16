from _decimal import Decimal
from django.db import models
from django.db.models import Count, Max, Min, Avg


class RealEstateListingManager(models.Manager):

    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        return self.values('location').annotate(
            most_visited_locations=Count('location')
        ).order_by('-most_visited_locations', 'id')[:2]


class VideoGameManager(models.Manager):

    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.annotate(highest_rate=Max('rating')).order_by('-rating').first()

    def lowest_rated_game(self):
        return self.annotate(lowest_rate=Min('rating')).order_by('rating').first()

    def average_rating(self):
        average_rate = self.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return f'{average_rate:.1f}'