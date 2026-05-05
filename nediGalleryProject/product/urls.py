
from django.urls import path


from nediGalleryProject.product.views import WhatWeOfferView, ProductListView, SingleProductView

urlpatterns = [
    path('what_we_offer/', WhatWeOfferView.as_view(), name='what-we-offer'),
    path('product_list/', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', SingleProductView.as_view(), name='single-product'),
    path('collection/<slug:collection_slug>/', ProductListView.as_view(), name='collection-products'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='category-products'),

]

