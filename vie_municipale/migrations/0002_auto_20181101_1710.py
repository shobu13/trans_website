# Generated by Django 2.1.2 on 2018-11-01 16:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vie_municipale', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('pdf', models.FileField(upload_to='bulletins/')),
            ],
        ),
        migrations.AddField(
            model_name='commission',
            name='suppleants',
            field=models.ManyToManyField(related_name='Commission_suppleants_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commission',
            name='titulaires',
            field=models.ManyToManyField(related_name='Commission_titulaire_set', to=settings.AUTH_USER_MODEL),
        ),
    ]