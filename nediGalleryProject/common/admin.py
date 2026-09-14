from django.contrib import admin

from nediGalleryProject.common.models import InstagramPics, ArtDescription


@admin.register(InstagramPics)
class InstagramPicsAdmin(admin.ModelAdmin):

    list_display = ('picture',)

@admin.register(ArtDescription)
class ArtDescriptionAdmin(admin.ModelAdmin):

    list_display = ('name', 'header', 'description', 'picture')
