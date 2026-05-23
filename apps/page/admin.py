from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from .models import HeroSection, ContactSection, ContactMessage

# Hero section register in admin
@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    fields = ['title', 'description', 'image']

# Contact section register in admin
@admin.register(ContactSection)
class ContactSectionAdmin(ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'email']
    fields = ['title', 'description', 'image', 'email', 'phone_number', 'address']

    def has_add_permission(self, request):
        return not ContactSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = ContactSection.objects.first()

        if obj:
            url = reverse(
                'admin:page_contactsection_change',
                args=[obj.id]
            )
            return redirect(url)

        return redirect(
            reverse('admin:page_contactsection_add')
        )
    
# Contact message in admin
@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message']