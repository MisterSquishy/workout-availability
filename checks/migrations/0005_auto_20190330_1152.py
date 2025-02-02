# Generated by Django 2.1.4 on 2019-03-30 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0004_check_location_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='location',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='check',
            name='location_id',
            field=models.CharField(db_index=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='check',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
