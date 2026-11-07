import smtplib

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from nediGalleryProject.common.forms import ContactUsForm
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


class ContactUsView(FormView):
    template_name = 'common/contact-us.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('contact-us')

    def form_valid(self, form):
        submitted_at = timezone.localtime()
        context = {
            "name": form.cleaned_data["name"],
            "email": form.cleaned_data["email"],
            "message": form.cleaned_data["message"],
            "submitted_at": submitted_at,
        }

        notification = EmailMultiAlternatives(
            subject="New message from the RANEDDI contact form",
            body=render_to_string(
                "common/emails/contact_notification.txt", context
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ENQUIRY_RECIPIENT_EMAIL],
            reply_to=[form.cleaned_data["email"]],
        )
        notification.attach_alternative(
            render_to_string(
                "common/emails/contact_notification.html", context
            ),
            "text/html",
        )

        try:
            if notification.send() != 1:
                raise smtplib.SMTPException("Contact notification was not sent.")
        except (OSError, smtplib.SMTPException):
            messages.error(
                self.request,
                "We could not send your message right now. Please try again later.",
            )
            return self.form_invalid(form)

        confirmation = EmailMultiAlternatives(
            subject="We received your message - RANEDDI",
            body=render_to_string(
                "common/emails/contact_confirmation.txt", context
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[form.cleaned_data["email"]],
            reply_to=[settings.ENQUIRY_REPLY_TO_EMAIL],
        )
        confirmation.attach_alternative(
            render_to_string(
                "common/emails/contact_confirmation.html", context
            ),
            "text/html",
        )

        try:
            if confirmation.send() != 1:
                raise smtplib.SMTPException("Contact confirmation was not sent.")
        except (OSError, smtplib.SMTPException):
            messages.error(
                self.request,
                "Your message was received, but we could not send a confirmation "
                "email. Please do not submit it again; we will respond as soon as "
                "possible.",
            )
            return super().form_valid(form)

        messages.success(
            self.request,
            "Thank you for contacting RANEDDI. Your message has been received.",
        )
        return super().form_valid(form)
