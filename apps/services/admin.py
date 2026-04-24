from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = [
        ('Основное', {
            'fields': ['name', 'slug', 'icon', 'order'],
        }),
        ('English (EN)', {
            'fields': ['name_en'],
            'classes': ['collapse'],
        }),
    ]


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'order']
    list_editable = ['is_published', 'order']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Основное', {
            'fields': ['category', 'title', 'slug', 'short_description', 'full_description', 'cover_image'],
        }),
        ('Детали', {
            'fields': ['tasks_solved', 'stages', 'duration', 'client_result'],
        }),
        ('English (EN)', {
            'fields': ['title_en', 'short_description_en', 'full_description_en'],
            'classes': ['collapse'],
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse'],
        }),
        ('Настройки', {
            'fields': ['is_published', 'order'],
        }),
    ]
