# Generated by Django 5.0.4 on 2024-04-22 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0003_alter_profile_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(6)]),
        ),
    ]
