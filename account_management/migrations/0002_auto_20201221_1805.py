# Generated by Django 2.2.8 on 2020-12-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default=False, max_length=30),
        ),
        migrations.AddField(
            model_name='historicalaccount',
            name='name',
            field=models.CharField(default=False, max_length=30),
        ),
    ]
