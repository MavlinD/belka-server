# Generated by Django 4.2 on 2023-05-05 12:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("indicators", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="log",
            name="date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
