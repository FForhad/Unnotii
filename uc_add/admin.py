from django.contrib import admin
from .models import Code, CodePDF
admin.site.site_header = "Unnoti Admin Panel"

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']

@admin.register(CodePDF)
class CodePDFAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'pdf']
