# Generated by Django 2.0.6 on 2018-06-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20180607_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='loaction',
            new_name='location',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='model',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='service_tag',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
