# Generated by Django 3.1 on 2020-10-23 13:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0027_auto_20201022_1822'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItemConsigliati',
            new_name='ItemConsigliato',
        ),
        migrations.AlterModelOptions(
            name='itemconsigliato',
            options={'verbose_name_plural': 'ItemConsigliati'},
        ),
    ]
