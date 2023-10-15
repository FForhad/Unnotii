from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CodeAddView, PaidPointView


urlpatterns = [
    path('api/add_codes/', CodeAddView.as_view(), name='add_codes_api'),
    path('api/recharge/', views.RechargeAPIView.as_view(), name='recharge'),
    path('api/paid_point/', PaidPointView.as_view(), name='paid_point'),
]

# This part is added to handle serving media files during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
