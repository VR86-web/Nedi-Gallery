from django.views.generic import TemplateView

from nediGalleryProject.common.models import (
    AboutInnerContentLeft,
    AboutInnerContentRight,
)

class AboutUsView(TemplateView):
    template_name = 'common/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_inner_content_left'] = AboutInnerContentLeft.objects.all()
        context['about_inner_content_right'] = AboutInnerContentRight.objects.all()
        return context


class ContactUsView(TemplateView):
    template_name = 'common/contact-us.html'
