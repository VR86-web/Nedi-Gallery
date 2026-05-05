from django.views.generic import ListView

from nediGalleryProject.product.models import Product, Collection


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = None

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collections'] = Collection.objects.all()

        return context
