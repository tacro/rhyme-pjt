# Generated by Django 2.0.2 on 2018-07-18 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verse',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]