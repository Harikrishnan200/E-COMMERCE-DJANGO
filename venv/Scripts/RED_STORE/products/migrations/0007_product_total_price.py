# Generated by Django 5.0.6 on 2024-06-28 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_size_subimage_productsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_price',
            field=models.FloatField(default=0.0),
        ),
    ]
