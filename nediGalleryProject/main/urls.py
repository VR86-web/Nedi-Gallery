from django.urls import path

from nediGalleryProject.main.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
