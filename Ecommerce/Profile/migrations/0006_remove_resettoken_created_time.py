# Generated by Django 5.0.4 on 2024-04-22 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_resettoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resettoken',
            name='created_time',
        ),
    ]