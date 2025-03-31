from django.urls import path, include
from .views import order_list
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet)  # Регистрируем ViewSet


urlpatterns = [
    path('', order_list, name='order_list'),
    path('', include(router.urls)),
]

