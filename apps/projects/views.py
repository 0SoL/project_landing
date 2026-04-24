from django.shortcuts import render, get_object_or_404
from .models import Project
from apps.seo.jsonld import project_schema, to_json


def project_list(request):
    client_type = request.GET.get('type', '')
    qs = Project.objects.filter(is_published=True)
    if client_type:
        qs = qs.filter(client_type=client_type)
    context = {
        'projects': qs,
        'active_type': client_type,
        'client_types': Project.CLIENT_TYPES,
        'meta_title': 'Проекты строительства железных дорог в Казахстане',
        'meta_description': 'Портфолио выполненных проектов: строительство и реконструкция железнодорожных путей для заводов, портов и терминалов.',
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    images = project.images.all()
    context = {
        'project': project,
        'images': images,
        'meta_title': project.meta_title or project.title,
        'meta_description': project.meta_description or project.task[:160],
        'schema_json': to_json(project_schema(project)),
    }
    return render(request, 'projects/detail.html', context)
