# Generated by Django 3.1 on 2020-10-02 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_address_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.ManyToManyField(null=True, to='accounts.Address'),
        ),
    ]