# Generated by Django 2.0.5 on 2018-06-07 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20180607_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='last_update',
            new_name='last_updated',
        ),
    ]
