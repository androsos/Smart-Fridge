# Generated by Django 2.1.7 on 2019-05-01 16:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField()),
                ('name', models.TextField(max_length=100)),
                ('product_name', models.TextField(default='unknown', max_length=100)),
                ('brand_name', models.TextField(default='unknown', max_length=100)),
                ('measure_type', models.TextField(default='unknown', max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('image', models.ImageField(blank='True', upload_to='barcode_image')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.IntegerField(primary_key=True, serialize=False)),
                ('category_name', models.TextField(max_length=100)),
                ('image', models.ImageField(blank='True', upload_to='category_image')),
            ],
        ),
        migrations.CreateModel(
            name='InFridgeItem',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('insert_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('barcode', models.ManyToManyField(to='UI.Barcode')),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ManyToManyField(to='UI.Barcode')),
            ],
        ),
        migrations.AddField(
            model_name='barcode',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='UI.Categories'),
        ),
    ]
