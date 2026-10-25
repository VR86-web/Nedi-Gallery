from django.contrib.sitemaps import Sitemap

from nediGalleryProject.blog.models import Blog
from nediGalleryProject.product.models import Category, Collection, Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, item):
        return item.updated_at


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Blog.objects.all()

    def lastmod(self, item):
        return item.updated_at


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.order_by("pk")


class CollectionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Collection.objects.order_by("pk")


sitemaps = {
    "products": ProductSitemap,
    "blog": BlogSitemap,
    "categories": CategorySitemap,
    "collections": CollectionSitemap,
}
