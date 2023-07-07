# Generated by Django 4.2.1 on 2023-07-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0016_alter_order_delivery_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_state',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_state',
            field=models.CharField(choices=[('ON DELIVERY', 'On Delivery'), ('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('CANCELED', 'Canceled')], default='UNPAID', max_length=50),
        ),
    ]