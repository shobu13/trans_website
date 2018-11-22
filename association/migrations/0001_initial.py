# Generated by Django 2.1.2 on 2018-11-22 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', markdownx.models.MarkdownxField()),
                ('president', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Association_president_set', to=settings.AUTH_USER_MODEL)),
                ('secretaire', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Association_secretaire_set', to=settings.AUTH_USER_MODEL)),
                ('tresorier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Association_tresorier_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
