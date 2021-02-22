# Generated by Django 3.1.7 on 2021-02-22 12:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_auto_20210222_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewcount',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='viewcount',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 2, 22, 12, 43, 33, 540947, tzinfo=utc), null=True),
        ),
    ]
