# Generated by Django 4.0.5 on 2022-07-05 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kithub', '0007_remove_kitingredient_bag_kitingredient_bagtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='kithub.part'),
        ),
    ]