from django.urls import path
from nediGalleryProject.blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
]