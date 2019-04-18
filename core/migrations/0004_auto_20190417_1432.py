# Generated by Django 2.1.5 on 2019-04-17 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190222_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elupicture',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='elu_picture', to=settings.AUTH_USER_MODEL),
        ),
    ]