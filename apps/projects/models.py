from django.db import models
from django.urls import reverse


class Project(models.Model):
    CLIENT_TYPES = [
        ('port', 'Порт'),
        ('factory', 'Завод'),
        ('terminal', 'Терминал'),
        ('logistics', 'Логистический центр'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название (EN)')
    slug = models.SlugField(unique=True, verbose_name='URL')
    client = models.CharField(max_length=200, blank=True, verbose_name='Клиент')
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPES, verbose_name='Тип клиента')
    year = models.PositiveIntegerField(verbose_name='Год')
    location = models.CharField(max_length=200, verbose_name='Локация')

    task = models.TextField(verbose_name='Задача клиента')
    task_en = models.TextField(blank=True, verbose_name='Задача клиента (EN)')
    solution = models.TextField(verbose_name='Наше решение')
    solution_en = models.TextField(blank=True, verbose_name='Наше решение (EN)')
    result = models.TextField(verbose_name='Результат')
    result_en = models.TextField(blank=True, verbose_name='Результат (EN)')

    track_length_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Длина пути (км)')
    switches_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='Стрелочных переводов')
    duration_months = models.PositiveIntegerField(null=True, blank=True, verbose_name='Продолжительность (мес.)')
    budget_display = models.CharField(max_length=100, blank=True, verbose_name='Бюджет (отображение)', help_text='Например: от 150 млн тг')

    cover_image = models.ImageField(upload_to='projects/covers/', verbose_name='Обложка')

    meta_title = models.CharField(max_length=70, blank=True, verbose_name='Meta Title')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta Description')

    is_featured = models.BooleanField(default=False, verbose_name='На главной')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['-year', 'order']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def get_client_type_display_ru(self):
        return dict(self.CLIENT_TYPES).get(self.client_type, '')


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name='Проект')
    image = models.ImageField(upload_to='projects/gallery/', verbose_name='Изображение')
    alt_text = models.CharField(max_length=300, blank=True, verbose_name='Alt текст')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото проекта'
        verbose_name_plural = 'Фото проекта'

    def __str__(self):
        return f'Фото: {self.project.title}'
