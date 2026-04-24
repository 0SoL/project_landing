from django.db import models


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='Название (EN)')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория техники'
        verbose_name_plural = 'Категории техники'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE, related_name='items', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    name_en = models.CharField(max_length=200, blank=True, verbose_name='Название (EN)')
    purpose = models.TextField(verbose_name='Назначение')
    purpose_en = models.TextField(blank=True, verbose_name='Назначение (EN)')
    application = models.TextField(blank=True, verbose_name='Где применяется')
    application_en = models.TextField(blank=True, verbose_name='Где применяется (EN)')
    specifications = models.JSONField(default=dict, verbose_name='Технические характеристики', help_text='{"Грузоподъемность": "25т"}')
    image = models.ImageField(upload_to='equipment/', blank=True, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликована')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Техника'
        verbose_name_plural = 'Техника'

    def __str__(self):
        return self.name
