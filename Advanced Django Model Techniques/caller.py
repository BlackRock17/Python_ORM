import os
import django
from _decimal import Decimal

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from django.core.exceptions import ValidationError

from main_app.models import Customer, Product, DiscountedProduct, SpiderHero, FlashHero

# Create queries within functions




