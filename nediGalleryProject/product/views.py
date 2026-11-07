import logging
import smtplib

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, DetailView, FormView

from nediGalleryProject.product.forms import ProductEnquiryForm
from nediGalleryProject.product.models import Product, Category, Collection


logger = logging.getLogger(__name__)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('form', ProductEnquiryForm())
        context.setdefault('show_enquiry_modal', False)
        return context


class ProductEnquiryView(FormView):
    form_class = ProductEnquiryForm
    template_name = 'product/product-single.html'
    http_method_names = ['post', 'options']

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['show_enquiry_modal'] = getattr(
            self, 'show_enquiry_modal', False
        )
        return context

    def form_invalid(self, form):
        self.show_enquiry_modal = True
        return super().form_invalid(form)

    def get_success_url(self):
        return self.product.get_absolute_url()

    def form_valid(self, form):
        context = {
            'product': self.product,
            'product_price': str(self.product.price)
            if self.product.price is not None
            else '',
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'message': form.cleaned_data['message'],
        }

        notification = EmailMultiAlternatives(
            subject=f"Product enquiry: {self.product.name}",
            body=render_to_string(
                'product/emails/enquiry_notification.txt', context
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ENQUIRY_RECIPIENT_EMAIL],
            reply_to=[form.cleaned_data['email']],
        )
        notification.attach_alternative(
            render_to_string(
                'product/emails/enquiry_notification.html', context
            ),
            'text/html',
        )

        try:
            if notification.send() != 1:
                raise smtplib.SMTPException(
                    'Product enquiry notification was not sent.'
                )
        except (OSError, smtplib.SMTPException):
            logger.exception(
                'Failed to send product enquiry notification for product %s',
                self.product.pk,
            )
            messages.error(
                self.request,
                'We could not submit your enquiry right now. Please try again later.',
            )
            return self.form_invalid(form)

        confirmation = EmailMultiAlternatives(
            subject=f"Your product enquiry - {self.product.name}",
            body=render_to_string(
                'product/emails/enquiry_confirmation.txt', context
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[form.cleaned_data['email']],
            reply_to=[settings.ENQUIRY_REPLY_TO_EMAIL],
        )
        confirmation.attach_alternative(
            render_to_string(
                'product/emails/enquiry_confirmation.html', context
            ),
            'text/html',
        )

        try:
            if confirmation.send() != 1:
                raise smtplib.SMTPException(
                    'Product enquiry confirmation was not sent.'
                )
        except (OSError, smtplib.SMTPException):
            logger.exception(
                'Failed to send product enquiry confirmation for product %s',
                self.product.pk,
            )
            messages.warning(
                self.request,
                'Your enquiry was received successfully, but we could not send '
                'a confirmation email. You do not need to submit it again; our '
                'team will contact you shortly.',
            )
            return super().form_valid(form)

        messages.success(
            self.request,
            'Thank you for your enquiry. Our team will contact you shortly.',
        )
        return super().form_valid(form)
