# Generated by Django 3.1 on 2020-10-23 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20201023_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='items',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.orderitem'),
        ),
    ]
