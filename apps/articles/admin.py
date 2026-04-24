from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ArticleCategory, Article


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = [
        ('Основное', {
            'fields': ['name', 'slug', 'order'],
        }),
        ('English (EN)', {
            'fields': ['name_en'],
            'classes': ['collapse'],
        }),
    ]


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ['title', 'category', 'published_at', 'is_featured', 'is_published']
    list_editable = ['is_featured', 'is_published']
    list_filter = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Основное', {
            'fields': ['category', 'title', 'slug', 'excerpt', 'content', 'cover_image', 'author', 'published_at'],
        }),
        ('English (EN)', {
            'fields': ['title_en', 'excerpt_en', 'content_en'],
            'classes': ['collapse'],
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse'],
        }),
        ('Настройки', {
            'fields': ['is_featured', 'is_published'],
        }),
    ]
