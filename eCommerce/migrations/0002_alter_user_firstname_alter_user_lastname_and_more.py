# Generated by Django 4.2.1 on 2023-05-13 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.CharField(max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(),
        ),
   
    ]
