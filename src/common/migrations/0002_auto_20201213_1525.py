# Generated by Django 2.2.6 on 2020-12-13 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(default=datetime.date(2020, 1, 1)),
        ),
    ]