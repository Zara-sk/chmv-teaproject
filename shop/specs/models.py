from django.db import models



class CategoryFeature(models.Model):
    """
    Характеристика категории
    """
    category = models.ForeignKey('main.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=124, verbose_name='Название характеристики')
    feature_filter_name = models.CharField(max_length=55 ,verbose_name='Имя для фильтра')
    unit = models.CharField(max_length=20, verbose_name='Единица измерения', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f'Категория: {self.category.name} | Характеристика: {self.feature_name}'


class FeatureValidator(models.Model):
    """
    Выборка значений для характеристики
    """
    category = models.ForeignKey('main.Category', verbose_name='Категория', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Ключ характеристики', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100, verbose_name='Значение')

    def __str__(self):
        return f'Категория: {self.category.name} | Характеристика: {self.feature_key.feature_name} | Значение: {self.valid_feature_value}'


class ProductFeatures(models.Model):
    """
    Набор  характеристик для товара mainapp
    """
    product = models.ForeignKey('main.Product', verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f'Товар: {self.product.title} | Характеристика: {self.feature.feature_name} | Значение: {self.value}'
