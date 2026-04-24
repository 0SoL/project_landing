from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Project, ProjectImage


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['title', 'client_type', 'year', 'location', 'is_featured', 'is_published', 'order']
    list_editable = ['is_featured', 'is_published', 'order']
    list_filter = ['client_type', 'is_published', 'is_featured', 'year']
    search_fields = ['title', 'client', 'location']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    fieldsets = [
        ('Основное', {
            'fields': ['title', 'slug', 'client', 'client_type', 'year', 'location', 'cover_image'],
        }),
        ('Описание проекта', {
            'fields': ['task', 'solution', 'result'],
        }),
        ('English (EN)', {
            'fields': ['title_en', 'task_en', 'solution_en', 'result_en'],
            'classes': ['collapse'],
        }),
        ('Параметры', {
            'fields': ['track_length_km', 'switches_count', 'duration_months', 'budget_display'],
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse'],
        }),
        ('Настройки', {
            'fields': ['is_featured', 'is_published', 'order'],
        }),
    ]
