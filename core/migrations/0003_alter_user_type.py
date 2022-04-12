# Generated by Django 3.2 on 2022-04-01 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_stationquotations_supplierquotations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'COMPANY'), (1, 'SUPPLIER'), (2, 'STATION'), (3, 'SUPPLIER EMPLOYEE')], default=0),
        ),
    ]