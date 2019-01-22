# Generated by Django 2.1.2 on 2019-01-09 09:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
        ('cadre_de_vie', '0005_auto_20190108_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='association.Association'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newpaper',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 1, 9, 9, 21, 13, 552785, tzinfo=utc)),
        ),
    ]
