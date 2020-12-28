# Generated by Django 2.2.8 on 2020-12-28 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_advertisement', '0004_bookad_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookad',
            name='ad_type',
            field=models.CharField(choices=[('sale', 'فروش'), ('buy', 'خرید')], db_index=True, default='sale', max_length=20, verbose_name='نوع درخواست'),
        ),
        migrations.AlterField(
            model_name='bookad',
            name='status',
            field=models.CharField(choices=[('approved', 'تایید شده'), ('disapproved', 'رد شده'), ('pending', 'در انتظار')], default='pending', max_length=20, verbose_name='وضعیت'),
        ),
    ]