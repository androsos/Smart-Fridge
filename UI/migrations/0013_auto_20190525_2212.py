# Generated by Django 2.1.7 on 2019-05-25 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UI', '0012_auto_20190524_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.IntegerField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('sent_date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='UI.Barcode')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
