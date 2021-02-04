# Generated by Django 3.1.6 on 2021-02-03 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='category',
            field=models.CharField(choices=[('photographer', 'photographer'), ('model', 'model'), ('H&M', 'H&M'), ('stylist', 'stylist'), ('other use', 'other use')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
