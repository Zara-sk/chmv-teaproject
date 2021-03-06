# Generated by Django 3.2.5 on 2021-10-25 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20211024_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_key', models.CharField(max_length=100, verbose_name='Ключ характеристики')),
                ('feature_name', models.CharField(max_length=255, verbose_name='Наименование характеристики')),
                ('postfix_for_value', models.CharField(blank=True, help_text=' как ::after ', max_length=255, null=True, verbose_name='Постфикс для значения')),
                ('use_in_filter', models.BooleanField(default=False, verbose_name='Использовать в фильрации товаров в шаблоне')),
                ('filter_type', models.CharField(choices=[('radio', 'Радиокнопка'), ('checkbox', 'Чекбокс')], default='checkbox', max_length=20, verbose_name='Тип фильтра')),
                ('filter_measure', models.CharField(blank=True, max_length=50, null=True, verbose_name='Еденица измерения для фильтра')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='Категория')),
            ],
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.CreateModel(
            name='ProductFeatureValidators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_value', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Значение характеристики')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='Категория')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.productfeatures', verbose_name='Характеристика')),
            ],
        ),
    ]
