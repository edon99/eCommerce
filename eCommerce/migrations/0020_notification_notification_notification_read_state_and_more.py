# Generated by Django 4.2.1 on 2023-07-13 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0019_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='read_state',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
