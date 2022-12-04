# Generated by Django 4.1.3 on 2022-12-02 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_delete_buyers_delete_vendors_buyer_vendor'),
        ('restaurant', '0003_rename_dishe_dish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='accounts.vendor'),
        ),
    ]