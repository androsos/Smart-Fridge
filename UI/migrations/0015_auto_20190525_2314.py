# Generated by Django 2.1.7 on 2019-05-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0014_auto_20190525_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='desc',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]