from django.urls import path
from .views import(
    GTokenAPIView,
    
)

urlpatterns = [
    path('api/lottery/', GTokenAPIView.as_view()),
]