from django.contrib import admin
from django import forms
from unfold.admin import ModelAdmin, StackedInline
from unfold.widgets import UnfoldAdminImageFieldWidget

from .models import User, Profile


class AvatarImageFieldWidget(UnfoldAdminImageFieldWidget):
    template_name = 'admin/widgets/avatar_image_input.html'


class ProfileInlineForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=AvatarImageFieldWidget)

    class Meta:
        model = Profile
        fields = '__all__'


# Profile inline for user model
class ProfileInline(StackedInline):
    model = Profile
    form = ProfileInlineForm
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# User register in admin
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    fields = ('email', 'is_active', 'is_staff', 'is_superuser')

    inlines = (ProfileInline,)
