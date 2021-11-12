# Generated by Django 3.2.5 on 2021-10-26 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0001_initial'),
        ('main', '0010_auto_20211026_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ManyToManyField(blank=True, related_name='features_for_product', to='specs.ProductFeatures'),
        ),
    ]
