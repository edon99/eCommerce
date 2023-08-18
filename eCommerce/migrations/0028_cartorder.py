# Generated by Django 4.2.1 on 2023-08-16 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0027_alter_cart_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('date_ordered', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.CharField(max_length=200, null=True)),
                ('phoneNumber', models.IntegerField()),
                ('payment_state', models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('CANCELED', 'Canceled')], default='UNPAID', max_length=50)),
                ('payment_method', models.CharField(choices=[('ON DELIVERY', 'On Delivery'), ('ONLINE', 'Online')], default='ON DELIVERY', max_length=50)),
                ('delivery_state', models.CharField(choices=[('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELED', 'Canceled'), ('PENDING', 'Pending')], default='PENDING', max_length=50)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eCommerce.cart')),
            ],
        ),
    ]
