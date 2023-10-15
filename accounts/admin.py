from django.contrib import admin
from .models import CustomUser

admin.site.site_header = "Unnoti Admin Panel"

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('phone_number', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)
