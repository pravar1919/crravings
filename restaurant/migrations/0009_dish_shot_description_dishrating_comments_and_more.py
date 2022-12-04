# Generated by Django 4.1.3 on 2022-12-03 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_restaurantrating_dishrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='shot_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dishrating',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurantrating',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
