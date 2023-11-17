import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models

from main_app.models import RealEstateListing, VideoGame, BillingInfo, Invoice, Programmer, Project, Technology

# Create and check models


