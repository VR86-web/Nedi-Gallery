from django.contrib import admin

from nediGalleryProject.common.models import InstagramPics


@admin.register(InstagramPics)
class InstagramPicsAdmin(admin.ModelAdmin):

    list_display = ('picture',)
