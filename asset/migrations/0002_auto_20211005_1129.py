# Generated by Django 3.2.6 on 2021-10-05 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Working'), (1, 'Repairing'), (2, 'Busted')], default=0),
        ),
        migrations.AlterField(
            model_name='asset',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Others'), (1, 'Desktop'), (2, 'Laptop'), (3, 'Printer')], default=0),
        ),
    ]
