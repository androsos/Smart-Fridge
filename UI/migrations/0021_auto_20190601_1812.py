# Generated by Django 2.1.7 on 2019-06-01 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0020_auto_20190531_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoorder',
            name='scheduled_date',
            field=models.TextField(null=True),
        ),
    ]
