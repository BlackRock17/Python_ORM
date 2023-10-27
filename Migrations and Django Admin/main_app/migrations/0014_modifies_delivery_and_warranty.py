# Generated by Django 4.2.4 on 2023-10-27 18:32
from datetime import timedelta
from django.db import migrations


def update_delivery_and_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')

    for order in order_model.objects.all():
        if order.status == 'Cancelled':
            order.delete()

    orders = order_model.objects.all()

    for order in orders:
        if order.status == 'Pending':
            order.delivery = order.order_date + timedelta(days=3)
        elif order.status == 'Completed':
            order.warranty = '24 months'
        # elif order.status == 'Cancelled':
        #     order.delete()

    order_model.objects.bulk_update(orders, ['delivery', 'warranty'])


def reverse_default_values(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')

    orders = order_model.objects.all()

    default_warranty = order_model._meta.get_field('warranty').default

    for order in orders:
        if order.status == 'Pending':
            order.delivery = None
        elif order.status == 'Completed':
            order.warranty = default_warranty

    order_model.objects.bulk_update(orders, ['delivery', 'warranty'])



class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0013_order"),
    ]

    operations = [
        migrations.RunPython(update_delivery_and_warranty, reverse_code=reverse_default_values)
    ]
