# Generated by Django 5.0.4 on 2024-04-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_placeorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placeorder',
            name='cart',
        ),
        migrations.AddField(
            model_name='placeorder',
            name='cart',
            field=models.ManyToManyField(to='Product.cart'),
        ),
    ]
