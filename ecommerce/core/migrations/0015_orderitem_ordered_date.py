# Generated by Django 3.1 on 2020-10-12 16:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201012_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 12, 16, 5, 10, 771574, tzinfo=utc)),
        ),
    ]