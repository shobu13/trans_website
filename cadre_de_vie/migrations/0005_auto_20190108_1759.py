# Generated by Django 2.1.2 on 2019-01-08 16:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_de_vie', '0004_auto_20190108_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newpaper',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 8, 16, 59, 35, 417514, tzinfo=utc)),
        ),
    ]