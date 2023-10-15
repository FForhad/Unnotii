from django.contrib import admin
from .models import GivenToken
admin.site.site_header = "Unnoti Admin Panel"
# Register your models here.
# admin.site.register(GivenToken)
@admin.register(GivenToken)
class GivenTokenAdmin(admin.ModelAdmin):
    list_display = ('gtoken', 'user','created_on')