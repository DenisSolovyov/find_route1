# Generated by Django 3.2.8 on 2021-10-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_alter_city_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название города'),
        ),
    ]
