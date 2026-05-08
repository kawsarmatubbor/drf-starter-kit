from django.contrib import admin
from django.urls import reverse
from unfold.admin import ModelAdmin, StackedInline
from .models import User, Profile


class ProfileInline(StackedInline):
    model = Profile
    extra = 0
    fields = ('first_name', 'last_name', 'phone_number', 'gender', 'bio', 'avatar')
    can_delete = False

    def has_delete_permission(self, request, obj=None):
        return False  


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("email", "is_active",)
    search_fields = ("email",)
    list_filter = ("is_active", "created_at")
    fields = ("email", "is_active")
    inlines = [ProfileInline]

class MyProfileAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        if request.user.is_authenticated:
            context['my_profile_url'] = reverse(
                'admin:user_user_change',
                args=[request.user.pk]
            )
        return context