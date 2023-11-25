import os
import django
from django.core.exceptions import ObjectDoesNotExist
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

    if products:
        products_str = '\n'.join(f'{p.name}, sold {p.sold_products} times' for p in products)
        return f'Top products:\n{products_str}'
    return ''

def apply_discounts():
    orders = Order.objects.annotate(
        num_products=Count('products')
    ).filter(
        num_products__gt=2, is_completed=False
    ).update(
        total_price=F('total_price') * 0.9
    )
    return f'Discount applied to {orders} orders.'


def complete_order():
    try:
        order = Order.objects.prefetch_related(
            'products'
        ).filter(
            is_completed=False
        ).latest(
            '-creation_date'
        )
    except ObjectDoesNotExist:
        return ''

    products = order.products.all()

    for product in products:
        if product.is_available:
            product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"

print(get_top_products())

