# Generated by Django 2.2.8 on 2020-12-28 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_advertisement', '0003_bookad_authorname'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookad',
            name='status',
            field=models.CharField(default='pending', max_length=20, verbose_name='وضعیت'),
        ),
    ]
