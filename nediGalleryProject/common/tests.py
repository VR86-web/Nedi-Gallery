import smtplib
from unittest.mock import patch

from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from nediGalleryProject.common.forms import ContactUsForm


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="office@raneddi.com",
    ENQUIRY_RECIPIENT_EMAIL="contact@raneddi.com",
    ENQUIRY_REPLY_TO_EMAIL="contact@raneddi.com",
)
class ContactUsTests(TestCase):
    valid_data = {
        "name": "Alex Example",
        "email": "alex@example.com",
        "message": "I would like to know more.",
    }

    def setUp(self):
        mail.outbox = []

    def test_form_requires_name_email_and_message(self):
        form = ContactUsForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(set(form.errors), {"name", "email", "message"})

    def test_form_rejects_invalid_email(self):
        form = ContactUsForm(
            data={**self.valid_data, "email": "not-an-email"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_valid_submission_sends_both_emails_and_redirects(self):
        response = self.client.post(reverse("contact-us"), self.valid_data)

        self.assertRedirects(response, reverse("contact-us"))
        self.assertEqual(len(mail.outbox), 2)

        notification, confirmation = mail.outbox
        self.assertEqual(notification.to, ["contact@raneddi.com"])
        self.assertEqual(notification.from_email, "office@raneddi.com")
        self.assertEqual(notification.reply_to, ["alex@example.com"])
        self.assertIn("Alex Example", notification.body)
        self.assertIn("alex@example.com", notification.body)
        self.assertIn("I would like to know more.", notification.body)
        self.assertIn("Submitted:", notification.body)
        self.assertEqual(len(notification.alternatives), 1)
        notification_html = notification.alternatives[0].content
        self.assertIn("Alex Example", notification_html)
        self.assertIn("I would like to know more.", notification_html)

        self.assertEqual(confirmation.to, ["alex@example.com"])
        self.assertEqual(confirmation.from_email, "office@raneddi.com")
        self.assertEqual(confirmation.reply_to, ["contact@raneddi.com"])
        self.assertIn("Thank you for contacting RANEDDI", confirmation.body)
        self.assertIn("received your message", confirmation.body)
        self.assertIn("respond as soon as possible", confirmation.body)

    def test_html_notification_escapes_customer_content(self):
        self.client.post(
            reverse("contact-us"),
            {**self.valid_data, "message": "<script>alert(1)</script>"},
        )

        notification_html = mail.outbox[0].alternatives[0].content
        self.assertNotIn("<script>", notification_html)
        self.assertIn("&lt;script&gt;", notification_html)

    def test_get_displays_csrf_protected_form(self):
        response = self.client.get(reverse("contact-us"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'name="message"')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'type="email"')

    def test_post_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(reverse("contact-us"), self.valid_data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(mail.outbox, [])

    def test_invalid_submission_preserves_values_and_sends_no_email(self):
        response = self.client.post(
            reverse("contact-us"),
            {**self.valid_data, "email": "invalid-email"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Alex Example"')
        self.assertContains(response, 'value="invalid-email"')
        self.assertContains(response, "Enter a valid email address.")
        self.assertEqual(mail.outbox, [])

    def test_internal_email_failure_shows_error_without_success(self):
        with patch(
            "nediGalleryProject.common.views.EmailMultiAlternatives.send",
            side_effect=smtplib.SMTPException("private SMTP detail"),
        ):
            response = self.client.post(
                reverse("contact-us"), self.valid_data
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We could not send your message")
        self.assertNotContains(response, "Thank you for contacting RANEDDI.")
        self.assertNotContains(response, "private SMTP detail")
        self.assertEqual(mail.outbox, [])

    def test_confirmation_failure_does_not_claim_full_success_or_invite_retry(self):
        with patch(
            "nediGalleryProject.common.views.EmailMultiAlternatives.send",
            side_effect=[1, smtplib.SMTPException("private SMTP detail")],
        ):
            response = self.client.post(
                reverse("contact-us"), self.valid_data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your message was received")
        self.assertContains(response, "Please do not submit it again")
        self.assertNotContains(
            response, "Your message has been received.</p>"
        )
        self.assertNotContains(response, "private SMTP detail")

    def test_honeypot_submission_is_rejected(self):
        response = self.client.post(
            reverse("contact-us"),
            {**self.valid_data, "website": "spam"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unable to submit your message")
        self.assertEqual(mail.outbox, [])
