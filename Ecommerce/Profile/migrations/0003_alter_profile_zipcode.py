# Generated by Django 5.0.4 on 2024-04-22 09:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_remove_profile_uuid_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(7), django.core.validators.MaxLengthValidator(7)]),
        ),
    ]
