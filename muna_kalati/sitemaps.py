from django.contrib.sitemaps import Sitemap
# from django.contrib.sitemaps.views import sitemap
from django.shortcuts import reverse
from .models import LatestUpdate, Category, PressRelease, OpenPosition

class LatestUpdateSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return LatestUpdate.objects.all()

    def lastmod(self, obj):
        return obj.created

# class CategorySitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.6

#     def items(self):
#         return Category.objects.all()

class PressReleaseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return PressRelease.objects.all()

    def lastmod(self, obj):
        return obj.created

class OpenPositionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return OpenPosition.objects.all()

# Add a static sitemap if needed
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['features', 'index', 'media_and_news', 'about_us']

    def location(self, item):
        return reverse(item)
