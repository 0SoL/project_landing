from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import EquipmentCategory, Equipment


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    fieldsets = [
        ('Основное', {
            'fields': ['name', 'order'],
        }),
        ('English (EN)', {
            'fields': ['name_en'],
            'classes': ['collapse'],
        }),
    ]


@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ['name', 'category', 'is_published', 'order']
    list_editable = ['is_published', 'order']
    list_filter = ['category', 'is_published']
    search_fields = ['name', 'purpose']
    fieldsets = [
        ('Основное', {
            'fields': ['category', 'name', 'purpose', 'application', 'image'],
        }),
        ('English (EN)', {
            'fields': ['name_en', 'purpose_en', 'application_en'],
            'classes': ['collapse'],
        }),
        ('Характеристики', {
            'fields': ['specifications'],
        }),
        ('Настройки', {
            'fields': ['is_published', 'order'],
        }),
    ]
