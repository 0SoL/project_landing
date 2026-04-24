from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory
from apps.seo.jsonld import service_schema, to_json


def service_list(request):
    categories = ServiceCategory.objects.prefetch_related('services').filter(services__is_published=True).distinct().order_by('order')
    context = {
        'categories': categories,
        'meta_title': 'Услуги по строительству железных дорог — РЖД-Инфра Казахстан',
        'meta_description': 'Полный цикл работ: проектирование, строительство, реконструкция и консалтинг в сфере железнодорожной инфраструктуры.',
    }
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_published=True)
    context = {
        'service': service,
        'meta_title': service.meta_title or service.title,
        'meta_description': service.meta_description or service.short_description,
        'schema_json': to_json(service_schema(service)),
    }
    return render(request, 'services/detail.html', context)
