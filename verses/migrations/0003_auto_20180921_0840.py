# Generated by Django 2.0.2 on 2018-09-21 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0002_auto_20180808_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='verse',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='verses.Verse'),
        ),
        migrations.AddField(
            model_name='verse',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
