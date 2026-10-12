from django.contrib import admin

from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
