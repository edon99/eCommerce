# Generated by Django 4.2.1 on 2023-08-21 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0035_alter_cart_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='quantities',
        ),
    ]