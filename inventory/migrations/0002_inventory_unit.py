# Generated by Django 3.2.6 on 2021-08-26 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='unit',
            field=models.CharField(default='item', max_length=255),
        ),
    ]
