from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.projects.models import Project
from apps.services.models import Service
from apps.articles.models import Article


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:faq',
            'core:contacts',
            'equipment:list',
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return None


class ServiceSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Service.objects.filter(is_published=True)


class ArticleSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at
