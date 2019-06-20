# Generated by Django 2.1.7 on 2019-06-02 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UI', '0022_auto_20190601_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('orderType', models.TextField(default='unknown', max_length=20)),
                ('date_sent', models.DateTimeField()),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemHistory',
            fields=[
                ('order_item_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UI.OrderHistory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='UI.Barcode')),
            ],
        ),
    ]