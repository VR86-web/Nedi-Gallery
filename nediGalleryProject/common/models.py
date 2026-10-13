from django.db import models


class InstagramPics(models.Model):

    picture = models.ImageField(
        upload_to='instagram_pics/',
        null=True,
        blank=True,
    )

    url = models.URLField(
        blank=True,
        null=True
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

    def __str__(self):
        return self.name or f"Art Description {self.id}"

class AboutInnerContentLeft(models.Model):

    header = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    content = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.header or f"About Inner Content Left {self.id}"

class AboutInnerContentRight(models.Model):

    header = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    content = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.header or f"About Inner Content Right {self.id}"
