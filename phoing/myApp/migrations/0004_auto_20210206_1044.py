# Generated by Django 3.1.5 on 2021-02-06 01:44

from django.db import migrations, models
import myApp.utils


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_merge_20210206_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='user.png', upload_to=myApp.utils.uuid_name_upload_to),
        ),
    ]
