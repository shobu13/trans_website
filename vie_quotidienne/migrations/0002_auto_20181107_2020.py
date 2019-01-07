# Generated by Django 2.1.2 on 2018-11-07 19:20

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('vie_quotidienne', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ouverture', models.DateTimeField()),
                ('fermeture', models.DateTimeField()),
                ('adresse', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='commerce',
            name='description',
            field=markdownx.models.MarkdownxField(),
        ),
    ]