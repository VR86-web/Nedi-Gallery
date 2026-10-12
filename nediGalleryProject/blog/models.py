from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Blog(models.Model):
    title = models.CharField(
        max_length=200
        )
    
    slug = models.SlugField(
        blank=True,
        max_length=200,
        unique_for_date='published',
        )
    
    picture = models.ImageField(
        upload_to='blog_pictures/'
        )
    
    content = models.TextField()

    published = models.DateTimeField(
        default=timezone.now
        )

    created_at = models.DateTimeField(
        auto_now_add=True
        )
    
    updated_at = models.DateTimeField(
        auto_now=True
        )

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]

    def get_absolute_url(self):
        return reverse(
            'blog:blog-detail',
            args=[
                self.published.year,
                self.published.month,
                self.published.day,
                self.slug,
            ]
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
