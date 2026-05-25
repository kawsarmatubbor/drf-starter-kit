from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from .models import Identity, SocialMedia

# Identity register in admin
@admin.register(Identity)
class IdentityAdmin(ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    fields = ['title', 'description', 'phone', 'email', 'address', 'logo', 'fav_icon']

    def has_add_permission(self, request):
        return not Identity.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = Identity.objects.first()

        if obj:
            url = reverse(
                'admin:system_setting_identity_change',
                args=[obj.id]
            )
            return redirect(url)

        return redirect(
            reverse('admin:system_setting_identity_add')
        )
    
# Social media register in admin
@admin.register(SocialMedia)
class SocialMediaAdmin(ModelAdmin):
    list_display = ['name', 'url', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'url']
    fields = ['name', 'url', 'icon']