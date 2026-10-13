from django.contrib import admin

from nediGalleryProject.common.models import AboutInnerContentLeft, AboutInnerContentRight, InstagramPics, ArtDescription


@admin.register(InstagramPics)
class InstagramPicsAdmin(admin.ModelAdmin):

    list_display = ('picture', 'url')

@admin.register(ArtDescription)
class ArtDescriptionAdmin(admin.ModelAdmin):

    list_display = ('name', 'header', 'picture')

@admin.register(AboutInnerContentLeft)
class AboutInnerContentLeftAdmin(admin.ModelAdmin):

    list_display = ('header', 'content')

@admin.register(AboutInnerContentRight)
class AboutInnerContentRightAdmin(admin.ModelAdmin):

    list_display = ('header', 'content')
