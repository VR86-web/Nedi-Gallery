import smtplib
from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from nediGalleryProject.product.models import Category, Product


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='office@raneddi.com',
    ENQUIRY_RECIPIENT_EMAIL='contact@raneddi.com',
    ENQUIRY_REPLY_TO_EMAIL='contact@raneddi.com',
)
class ProductEnquiryTests(TestCase):
    valid_data = {
        'name': 'Alex Example',
        'email': 'alex@example.com',
        'message': 'I am interested in this product.',
    }

    def setUp(self):
        mail.outbox = []
        self.category = Category.objects.create(name='Accessories')
        self.product = Product.objects.create(
            name='Silver Necklace',
            price=Decimal('49.95'),
            category=self.category,
        )
        self.other_product = Product.objects.create(
            name='Gold Bracelet',
            price=Decimal('85.00'),
            category=self.category,
        )
        self.enquiry_url = reverse(
            'product:product-enquiry', kwargs={'slug': self.product.slug}
        )
        self.detail_url = self.product.get_absolute_url()

    def test_product_page_shows_price_and_bootstrap_enquiry_modal(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Silver Necklace | €49.95')
        self.assertContains(response, 'ENQUIRE ABOUT THIS PRODUCT')
        self.assertContains(response, 'data-toggle="modal"')
        self.assertContains(response, 'Interested in this product?')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertNotContains(response, 'ADD TO CART')

    def test_valid_submission_sends_product_enquiry_and_confirmation(self):
        response = self.client.post(self.enquiry_url, self.valid_data)

        self.assertRedirects(response, self.detail_url)
        self.assertEqual(len(mail.outbox), 2)

        notification, confirmation = mail.outbox
        self.assertEqual(notification.to, ['contact@raneddi.com'])
        self.assertEqual(notification.from_email, 'office@raneddi.com')
        self.assertEqual(notification.reply_to, ['alex@example.com'])
        self.assertIn('Silver Necklace', notification.body)
        self.assertIn('€49.95', notification.body)
        self.assertIn('Alex Example', notification.body)
        self.assertIn('alex@example.com', notification.body)
        self.assertIn('I am interested in this product.', notification.body)
        self.assertIn('not a confirmed order', notification.body)

        self.assertEqual(confirmation.to, ['alex@example.com'])
        self.assertEqual(confirmation.from_email, 'office@raneddi.com')
        self.assertEqual(confirmation.reply_to, ['contact@raneddi.com'])
        self.assertIn('Silver Necklace', confirmation.body)
        self.assertIn('€49.95', confirmation.body)
        self.assertIn('Thank you for your enquiry', confirmation.body)
        self.assertIn('contact you shortly', confirmation.body)
        self.assertIn('not a confirmed order or purchase', confirmation.body)

        self.assertEqual(len(notification.alternatives), 1)
        self.assertEqual(len(confirmation.alternatives), 1)
        self.assertIn('Silver Necklace', notification.alternatives[0].content)
        self.assertIn('€49.95', notification.alternatives[0].content)
        self.assertIn('Silver Necklace', confirmation.alternatives[0].content)
        self.assertIn('€49.95', confirmation.alternatives[0].content)

    def test_product_is_taken_from_url_not_submitted_values(self):
        response = self.client.post(
            self.enquiry_url,
            {
                **self.valid_data,
                'product_id': str(self.other_product.pk),
                'product_name': self.other_product.name,
                'price': str(self.other_product.price),
            },
        )

        self.assertRedirects(response, self.detail_url)
        self.assertIn('Silver Necklace', mail.outbox[0].body)
        self.assertIn('€49.95', mail.outbox[0].body)
        self.assertNotIn('Gold Bracelet', mail.outbox[0].body)
        self.assertNotIn('€85.00', mail.outbox[0].body)

    def test_invalid_name_email_and_message_do_not_send_email(self):
        invalid_submissions = (
            ({**self.valid_data, 'name': ''}, 'name'),
            ({**self.valid_data, 'email': 'invalid-email'}, 'email'),
            ({**self.valid_data, 'message': ''}, 'message'),
        )

        for data, invalid_field in invalid_submissions:
            with self.subTest(field=invalid_field):
                response = self.client.post(self.enquiry_url, data)

                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].has_error(invalid_field))
                self.assertTrue(response.context['show_enquiry_modal'])

        self.assertEqual(mail.outbox, [])

    def test_form_rejects_fields_exceeding_maximum_lengths(self):
        invalid_submissions = (
            {**self.valid_data, 'name': 'n' * 101},
            {**self.valid_data, 'email': f"{'a' * 250}@example.com"},
            {**self.valid_data, 'message': 'm' * 5001},
        )

        for data in invalid_submissions:
            with self.subTest(data_length=len(data.get('message', data.get('name', data.get('email', ''))))):
                response = self.client.post(self.enquiry_url, data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)

        self.assertEqual(mail.outbox, [])

    def test_html_emails_escape_customer_content(self):
        self.client.post(
            self.enquiry_url,
            {**self.valid_data, 'message': '<script>alert(1)</script>'},
        )

        notification_html = mail.outbox[0].alternatives[0].content
        confirmation_html = mail.outbox[1].alternatives[0].content
        self.assertNotIn('<script>', notification_html)
        self.assertNotIn('<script>', confirmation_html)
        self.assertIn('&lt;script&gt;', notification_html)

    def test_internal_notification_failure_shows_error_without_sending_confirmation(self):
        with self.assertLogs(
            'nediGalleryProject.product.views', level='ERROR'
        ), patch(
            'nediGalleryProject.product.views.EmailMultiAlternatives.send',
            side_effect=smtplib.SMTPException('private SMTP detail'),
        ):
            response = self.client.post(self.enquiry_url, self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'We could not submit your enquiry')
        self.assertNotContains(response, 'private SMTP detail')
        self.assertEqual(mail.outbox, [])

    def test_confirmation_failure_says_enquiry_was_received(self):
        with self.assertLogs(
            'nediGalleryProject.product.views', level='ERROR'
        ), patch(
            'nediGalleryProject.product.views.EmailMultiAlternatives.send',
            side_effect=[1, smtplib.SMTPException('private SMTP detail')],
        ):
            response = self.client.post(
                self.enquiry_url, self.valid_data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your enquiry was received successfully')
        self.assertContains(response, 'You do not need to submit it again')
        self.assertNotContains(response, 'private SMTP detail')

    def test_post_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(self.enquiry_url, self.valid_data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(mail.outbox, [])
