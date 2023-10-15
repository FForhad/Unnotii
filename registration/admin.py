from django.contrib import admin
from .models import UserProfile
admin.site.site_header = "Unnoti Admin Panel"

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp_verified')
    list_filter = ('otp_verified',)
    search_fields = ('phone_number',)

admin.site.register(UserProfile, UserProfileAdmin)
