from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from rest_framework import viewsets
from .serializers import OrderSerializer
# Create your views here.

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Выбираем все заказы
    serializer_class = OrderSerializer  # Используем наш сериализатор
