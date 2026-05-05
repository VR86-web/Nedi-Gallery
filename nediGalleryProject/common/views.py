from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    template_name = 'common/about.html'


class ContactUsView(TemplateView):
    template_name = 'common/contact-us.html'
