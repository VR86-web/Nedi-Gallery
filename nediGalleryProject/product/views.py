from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView

from nediGalleryProject.product.models import Product, Category, Collection


class WhatWeOfferView(TemplateView):
    template_name = 'product/what-we-offer.html'


class ProductListView(ListView):
    model = Product
    template_name = 'product/product-list.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()

        category_slug = self.kwargs.get('category_slug')
        collection_slug = self.kwargs.get('collection_slug')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if collection_slug:
            queryset = queryset.filter(collection__slug=collection_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs.get('category_slug')
        collection_slug = self.kwargs.get('collection_slug')

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            context['page_name'] = category.name.capitalize()
            context['description'] = category.description
            context['background_picture'] = category.category_picture

        elif collection_slug:
            collection = Collection.objects.get(slug=collection_slug)
            context['page_name'] = collection.name
            context['description'] = collection.description
            context['background_picture'] = collection.picture

        else:
            context['page_name'] = 'Shop'
            context['description'] = None
            context['background_picture'] = None

        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        )

        context['collections'] = Collection.objects.all()

        return context


class SingleProductView(DetailView):
    model = Product
    template_name = 'product/product-single.html'
    context_object_name = 'product'


