import json

ORGANIZATION = {
    '@type': 'Organization',
    'name': 'РЖД-Инфра Казахстан',
    'description': 'Проектирование, строительство и реконструкция железнодорожных путей для промышленных предприятий, портов и логистических терминалов Казахстана.',
    'areaServed': 'Kazakhstan',
    'serviceType': [
        'Строительство железнодорожных путей',
        'Реконструкция железнодорожных путей',
        'Проектирование железнодорожных путей',
        'Укладка рельсов',
    ],
    'address': {
        '@type': 'PostalAddress',
        'addressCountry': 'KZ',
    },
}


def organization_schema():
    return {'@context': 'https://schema.org', **ORGANIZATION}


def faq_schema(items):
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': item.question,
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': item.answer,
                },
            }
            for item in items
        ],
    }


def article_schema(article):
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': article.title,
        'description': article.excerpt,
        'author': {
            '@type': 'Person',
            'name': article.author or 'Редакция',
        },
        'datePublished': str(article.published_at),
        'publisher': ORGANIZATION,
    }


def service_schema(service):
    return {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': service.title,
        'description': service.short_description,
        'provider': ORGANIZATION,
        'areaServed': 'Kazakhstan',
        'serviceType': service.title,
    }


def project_schema(project):
    return {
        '@context': 'https://schema.org',
        '@type': 'Project',
        'name': project.title,
        'description': project.task,
        'location': {
            '@type': 'Place',
            'name': project.location,
        },
        'provider': ORGANIZATION,
    }


def to_json(schema_dict):
    return json.dumps(schema_dict, ensure_ascii=False, indent=2)
