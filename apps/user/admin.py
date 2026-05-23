from django.contrib import admin
from .models import User, Profile

# Profile inline for user model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# User register in admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    fields = ('email', 'is_active', 'is_staff', 'is_superuser')

    inlines = (ProfileInline,)