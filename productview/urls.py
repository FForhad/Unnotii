from django.urls import path
from .views import(
    ProductItemAPIView,
    ProductItemsAIPView,
    ProductPointAPIView,
    ProductPointsAIPView,
)

urlpatterns = [
    path('api/product/', ProductItemAPIView.as_view()),
    path('api/product/<int:pk>', ProductItemsAIPView.as_view()),
    path('api/productpoint/', ProductPointAPIView.as_view()),
    path('api/productpoint/<int:pk>', ProductPointsAIPView.as_view()),
]