# Generated by Django 4.2.1 on 2023-08-21 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0037_cart_quantities'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartQuantities',
        ),
    ]
