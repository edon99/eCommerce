# Generated by Django 4.2.1 on 2023-08-20 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0033_cart_cartquantities_cartorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantities',
            field=models.ManyToManyField(related_name='CartQuantities', to='eCommerce.cartquantities'),
        ),
    ]
