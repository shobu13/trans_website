# Generated by Django 2.1.2 on 2019-01-09 09:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_de_vie', '0007_auto_20190109_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newpaper',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 9, 9, 22, 42, 623237, tzinfo=utc)),
        ),
    ]