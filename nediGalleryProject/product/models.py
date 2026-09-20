from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse


class Product(models.Model):

    name = models.CharField(
        max_length=50,
    )

    picture = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        on_delete=models.PROTECT,
        to='Category',
        related_name='products',
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    short_description = models.TextField(
        blank=True,
        null=True,
    )

    collection = models.ForeignKey(
        'Collection',
        on_delete=models.PROTECT,
        related_name="products",
        blank=True,
        null=True,
    )

    published = models.DateTimeField(
        default=timezone.now
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]

    def get_absolute_url(self):

        return reverse('product:single-product', kwargs={
            'slug': self.slug,
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Collection(models.Model):

    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        upload_to="collections/",
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:collection-products", kwargs={"collection_slug": self.slug})
    


class Category(models.Model):

    name = models.CharField(
        max_length=50,
    )

    description = models.TextField(
            blank=True,
            null=True,
    )

    category_picture = models.ImageField(
    upload_to='category_backgrounds/',
    null=True,
    blank=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:category-products", kwargs={"category_slug": self.slug})
    
