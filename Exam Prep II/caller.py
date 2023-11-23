import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Profile, Order


# Create and run your queries within functions


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    query = (Q(full_name__icontains=search_string)
             | Q(email__icontains=search_string)
             | Q(phone_number__icontains=search_string))

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles:
        return ""

    result = []

    for profile in profiles.annotate(num_orders=Count('order_profile')):
        result.append(
            f'Profile: {profile.full_name},'
            f' email: {profile.email},'
            f' phone number: {profile.phone_number},'
            f' orders: {profile.num_orders}'
        )

    return '\n'.join(result)

