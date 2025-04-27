from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    order_list,
    order_create,
    order_update,
    order_delete,
    order_update_status,   # ✅ Добавляем новую вьюшку
    revenue_report,
    revenue,               # ✅ Добавляем новую вьюшку для расчета выручки
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')  # API orders/

urlpatterns = [
    path('', order_list, name='order_list'),                        # Список заказов
    path('order/create/', order_create, name='order_create'),       # Создание заказа
    path('order/update/<int:pk>/', order_update, name='order_update'), # Обновление заказа
    path('order/update-status/<int:pk>/', order_update_status, name='order_update_status'), # ✅ Обновление только статуса
    path('order/delete/<int:pk>/', order_delete, name='order_delete'), # Удаление заказа
    path('revenue/', revenue, name='revenue'),                      # ✅ Расчет выручки (с выбором дат)
    path('revenue/report/', revenue_report, name='revenue_report'), # Отчет по оплаченным заказам
    path('api/', include(router.urls)),                             # API маршруты
]
