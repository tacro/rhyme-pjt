# Generated by Django 2.0.2 on 2018-08-07 13:50

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_mcname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mcname',
            field=models.CharField(default=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=50, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username'), max_length=50, verbose_name='MC name'),
        ),
    ]
