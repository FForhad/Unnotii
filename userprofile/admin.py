from django.contrib import admin
from .models import Profile, RechargeLog
admin.site.site_header = "Unnoti Admin Panel"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'points', 'created_on', 'updated_on')
    search_fields = ('name', 'user__phone_number')

@admin.register(RechargeLog)
class RechargeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'value', 'date')
