# Generated by Django 4.2.1 on 2023-08-21 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0036_remove_cart_quantities'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantities',
            field=models.JSONField(default=dict),
        ),
    ]
