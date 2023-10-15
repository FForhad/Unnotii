# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('accounts.urls')),
    path('', include('productview.urls')),
    # path('', include('pointlogs.urls')),
    path('', include('userprofile.urls')),
    path('', include('lottery.urls')),
    # path('', include('recharge.urls')),
    path('', include('registration.urls')),
    path('', include('uc_add.urls')),
    path('', include('extra.urls')),
]
