# Generated by Django 3.1 on 2020-10-12 19:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_orderitem_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='ordered_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]