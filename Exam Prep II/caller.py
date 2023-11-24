import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Profile, Order, Product


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


def get_loyal_profiles():

    result = []

    for p in Profile.objects.get_regular_customers():
        result.append(f'Profile: {p.full_name}, orders: {p.num_orders}')

    return '\n'.join(result) if result else ''


def get_last_sold_products():
    result = []

    order = Order.objects.prefetch_related('products').last()

    if order is None:
        return ''

    products = order.products.all().order_by('name')

    if products:
        for p in products:
            result.append(f'{p.name}')

        return f'Last sold products: {", ".join(result)}'
    return ''


def get_top_products():
    products = Product.objects.prefetch_related(
        'order_products__products'
    ).annotate(
        sold_products=Count('order_products')
    ).filter(
        sold_products__gt=0
    ).order_by(
        '-sold_products',
        'name'
    )[:5]

    result = 'Top products: \n'

    if products is None:
        return ''

    for p in products:
        result += f'{p.name}, sold {p.sold_products} times' + '\n'

    return result


def apply_discounts():
    orders = Order.objects.annotate(
        num_products=Count('products')
    ).filter(
        num_products__gt=2, is_completed=False
    ).update(
        total_price=F('total_price') * 0.9
    )
    return f'Discount applied to {orders} orders.'


def abv():
    a = Order.objects.prefetch_related('products').all()

    return a.filter(products__description='Hot', is_completed=False).update(total_price=1)

print(abv())