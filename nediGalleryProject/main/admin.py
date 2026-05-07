from django.contrib import admin

from nediGalleryProject.main.models import OwnerInfo


@admin.register(OwnerInfo)
class OwnerInfoAdmin(admin.ModelAdmin):

    list_display = ('owner_name', 'owner_picture', 'created_at', 'owner_description',)