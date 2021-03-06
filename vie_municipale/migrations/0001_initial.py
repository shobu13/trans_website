# Generated by Django 2.1.5 on 2019-07-03 08:41

from django.conf import settings
from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=250)),
                ('description', markdownx.models.MarkdownxField()),
                ('suppleants', models.ManyToManyField(related_name='commission_suppleants', to=settings.AUTH_USER_MODEL)),
                ('titulaires', models.ManyToManyField(related_name='commission_titulaire', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Conseil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=250)),
                ('texte', markdownx.models.MarkdownxField()),
                ('pdf', models.FileField(upload_to='conseil_pdf/')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=250)),
                ('texte', markdownx.models.MarkdownxField()),
            ],
        ),
    ]
