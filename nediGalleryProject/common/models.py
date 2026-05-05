from django.db import models


class InstagramPics(models.Model):

    picture = models.ImageField(
        upload_to='instagram_pics/',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Instagram Pic {self.id}"


