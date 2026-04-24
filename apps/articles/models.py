from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='Название (EN)')
    slug = models.SlugField(unique=True, verbose_name='URL')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория статей'
        verbose_name_plural = 'Категории статей'

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles', verbose_name='Категория')
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    title_en = models.CharField(max_length=250, blank=True, verbose_name='Заголовок (EN)')
    slug = models.SlugField(unique=True, verbose_name='URL')
    excerpt = models.TextField(max_length=350, verbose_name='Анонс')
    excerpt_en = models.TextField(max_length=350, blank=True, verbose_name='Анонс (EN)')
    content = models.TextField(verbose_name='Содержание (HTML)')
    content_en = models.TextField(blank=True, verbose_name='Содержание (HTML) (EN)')
    cover_image = models.ImageField(upload_to='articles/', blank=True, verbose_name='Обложка')
    author = models.CharField(max_length=100, blank=True, verbose_name='Автор')
    published_at = models.DateField(verbose_name='Дата публикации')
    meta_title = models.CharField(max_length=70, blank=True, verbose_name='Meta Title')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta Description')
    is_published = models.BooleanField(default=True, verbose_name='Опубликована')
    is_featured = models.BooleanField(default=False, verbose_name='Главная')

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})
