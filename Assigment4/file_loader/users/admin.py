from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Prevent deletion of profiles
    verbose_name_plural = 'Profiles'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)