from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Contact

@admin.register(Contact)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'is_replied')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    fields = ('name', 'email', 'phone', 'message', 'is_replied', 'is_active')
    readonly_fields = ('email', 'phone', 'message', 'created_at')
