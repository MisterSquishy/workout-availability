# Generated by Django 2.1.4 on 2019-03-30 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0003_auto_20190328_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='location_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
