# Generated by Django 3.1.2 on 2021-08-30 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventory_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
