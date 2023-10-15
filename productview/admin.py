from django.contrib import admin
from .models import ProductItem,ProductPoint
admin.site.site_header = "Unnoti Admin Panel"
# Register your models here.
# admin.site.register(ProductItem)
@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','created_on',)

# admin.site.register(ProductPoint)
@admin.register(ProductPoint)
class ProductPointAdmin(admin.ModelAdmin):
    list_display = ('title', 'point',)
