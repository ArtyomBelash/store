# Generated by Django 5.0.3 on 2024-03-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/<django.db.models.fields.CharField>', verbose_name=''),
        ),
    ]
