import os
from datetime import date

import django
from django.core.exceptions import ValidationError

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Mage, Necromancer, Message, UserProfile, Student, CreditCard, Hotel, Room, \
    SpecialReservation





