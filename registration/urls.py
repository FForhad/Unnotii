from django.urls import path
from . import views

from .views import(
    CustomLoginView,
    
)

urlpatterns = [
    path('api/register/', views.register_user, name='register_user'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    path('api/login/', CustomLoginView.as_view(), name='login'),
    #path('api/logout/', CustomLogoutView.as_view(), name='logiout'),
]
