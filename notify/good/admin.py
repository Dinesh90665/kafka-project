from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import NotificationPreference

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "method")  # Show in list view
    list_filter = ("topic", "method")           # Filters in sidebar
    search_fields = ("user__username", "topic", "method")  # Search bar






from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'phone_number')  # show email via method
    search_fields = ('user__username', 'user__email', 'phone_number')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
