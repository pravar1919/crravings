# Generated by Django 4.1.3 on 2022-12-04 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_objectviewed_restra_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objectviewed',
            old_name='restra_id',
            new_name='model_name',
        ),
        migrations.AddField(
            model_name='objectviewed',
            name='model_product_id',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
