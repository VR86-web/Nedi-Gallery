from django.urls import path

from nediGalleryProject.common.views import AboutUsView, ContactUsView

urlpatterns = [
    path('about_us/', AboutUsView.as_view(), name='about-us'),
    path('contact_us/', ContactUsView.as_view(), name='contact-us'),

]

