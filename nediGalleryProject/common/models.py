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

class ArtDescription(models.Model):

    picture = models.ImageField(
            upload_to='art_description_pics/',
            null=True,
            blank=True,
        )

    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    header = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name or f"Art Description {self.id}"
