# Generated by Django 4.0.5 on 2022-06-14 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kithub', '0004_purchase_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitingredient',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
