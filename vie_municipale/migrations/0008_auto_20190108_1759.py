# Generated by Django 2.1.2 on 2019-01-08 16:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vie_municipale', '0007_auto_20190108_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 8, 16, 59, 35, 409536, tzinfo=utc)),
        ),
    ]