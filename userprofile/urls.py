from django.urls import path
from .views import ProfileAPIView, ProfilesAIPView, RechargeLogAPIView

urlpatterns = [
    path('api/profile/', ProfileAPIView.as_view()),
    path('api/profile/<int:pk>', ProfilesAIPView.as_view()),
    path('api/recharge_log/', RechargeLogAPIView.as_view()), # New endpoint
    # ... (your other endpoints)
]
