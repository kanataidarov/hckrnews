# Generated by Django 2.2.17 on 2021-01-18 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_auto_20210118_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='order',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
