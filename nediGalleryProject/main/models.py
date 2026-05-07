from django.db import models


class OwnerInfo(models.Model):

    owner_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    owner_picture = models.ImageField(
        upload_to='instagram_pics/',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    owner_description = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.owner_name
