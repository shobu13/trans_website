# Generated by Django 2.1.2 on 2019-01-09 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vie_municipale', '0012_auto_20190109_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]