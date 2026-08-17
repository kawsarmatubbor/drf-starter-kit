from django.contrib import admin
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminImageFieldWidget
from .models import Identity, SocialMedia


class IdentityImageFieldWidget(UnfoldAdminImageFieldWidget):
    template_name = 'admin/widgets/identity_image_input.html'


class IdentityAdminForm(forms.ModelForm):
    logo = forms.ImageField(required=False, widget=IdentityImageFieldWidget)
    fav_icon = forms.ImageField(required=False, widget=IdentityImageFieldWidget)

    class Meta:
        model = Identity
        fields = '__all__'


class SocialMediaImageFieldWidget(UnfoldAdminImageFieldWidget):
    template_name = 'admin/widgets/identity_image_input.html'


class SocialMediaAdminForm(forms.ModelForm):
    icon = forms.ImageField(required=False, widget=SocialMediaImageFieldWidget)

    class Meta:
        model = SocialMedia
        fields = '__all__'

# Identity register in admin
@admin.register(Identity)
class IdentityAdmin(ModelAdmin):
    form = IdentityAdminForm
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
    form = SocialMediaAdminForm
    list_display = ['name', 'url', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'url']
    fields = ['name', 'url', 'icon']
