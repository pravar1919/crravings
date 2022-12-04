# Generated by Django 4.1.3 on 2022-12-04 07:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_alter_dish_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishrating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dishrating',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='restaurantrating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurantrating',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]