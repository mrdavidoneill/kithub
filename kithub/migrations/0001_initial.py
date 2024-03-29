# Generated by Django 4.0.5 on 2022-06-13 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BagType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='KitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('shop', models.CharField(max_length=255)),
                ('shop_part_no', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=5, max_digits=10)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.part')),
            ],
        ),
        migrations.CreateModel(
            name='KitContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.bag')),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.kit')),
            ],
        ),
        migrations.AddField(
            model_name='kit',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.kittype'),
        ),
        migrations.CreateModel(
            name='BagContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.bag')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.part')),
            ],
        ),
        migrations.AddField(
            model_name='bag',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kithub.bagtype'),
        ),
    ]
