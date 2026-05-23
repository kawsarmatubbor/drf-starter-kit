from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import HeroSection

# Hero section register in admin
@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'image']
