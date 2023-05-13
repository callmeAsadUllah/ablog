from django.contrib.sitemaps import Sitemap


from blog.models import (
    PostModel
)


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return PostModel.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_on