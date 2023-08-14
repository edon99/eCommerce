# Generated by Django 4.2.1 on 2023-07-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0022_order_payment_method_alter_order_payment_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('ON DELIVERY', 'On Delivery'), ('ONLINE', 'Online')], default='ON DELIVERY', max_length=50),
        ),
    ]
