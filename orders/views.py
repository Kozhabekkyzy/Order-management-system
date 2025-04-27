from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.utils import timezone  # ✅ для фильтрации по датам

from .models import Order, Status, Item
from orders.serializers import OrderSerializer
from orders.actions import order_total_price
from .forms import OrderForm
from .actions import order_total_price

# HTML-страница списка заказов
def order_list(request):
    status_filter = request.GET.get('status', None)
    orders = Order.objects.all()

    # Фильтрация заказов по статусу
    if status_filter:
        orders = orders.filter(status__id=status_filter)

    # Получаем все доступные статусы
    statuses = Status.objects.all()

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'statuses': statuses,
        'selected_status': status_filter
    })


# HTML-страница создания заказа
def order_create(request):
    items = Item.objects.all()  # Все доступные блюда
    statuses = Status.objects.all()  # Все возможные статусы
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_total_price(order)  # пересчитать сумму после сохранения
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Добавить заказ',
        'items': items,   # Передаем блюда
        'statuses': statuses  # Передаем статусы
    })



# HTML-страница изменения заказа
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = Item.objects.all()  # Все доступные блюда
    statuses = Status.objects.all()  # Все возможные статусы

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            order_total_price(order)  # обновить сумму
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {
        'form': form,
        'title': 'Изменить заказ',
        'items': items,  # Передаем блюда
        'statuses': statuses  # Передаем статусы
    })
# HTML-страница удаления заказа
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})

# API через DRF
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметр 'status' из запроса
        status_id = self.request.query_params.get('status', None)

        # Если status_id передан в запросе, фильтруем заказы
        if status_id:
            queryset = queryset.filter(status__id=status_id)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        items = validated_data.pop('items_ids')
        status_obj = validated_data.pop('status_id')

        order = Order.objects.create(status=status_obj, **validated_data)
        order.items.add(*items)
        order_total_price(order)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        order_instance = self.get_object()
        serializer = self.get_serializer(order_instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        item_objs = validated_data.pop('items_ids', None)
        status_obj = validated_data.pop('status_id', None)

        if status_obj is not None:
            order_instance.status = status_obj

        if item_objs is not None:
            order_instance.items.clear()
            order_instance.items.add(*item_objs)

        order_instance.save()
        order_total_price(order_instance)

        return Response(OrderSerializer(order_instance).data)


def revenue_report(request):
    # Фильтруем только оплаченные заказы
    paid_orders = Order.objects.filter(status__name="оплачено")

    # Считаем общую сумму выручки
    total_revenue = sum(order.total_price for order in paid_orders)

    return render(request, 'orders/revenue_report.html', {
        'paid_orders': paid_orders,
        'total_revenue': total_revenue
    })


def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    statuses = Status.objects.all()

    if request.method == 'POST':
        status_id = request.POST.get('status')
        status_obj = get_object_or_404(Status, id=status_id)
        order.status = status_obj
        order.save()
        return redirect('order_list')

    return render(request, 'orders/order_update_status.html', {
        'order': order,
        'statuses': statuses
    })


def revenue(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            paid_orders = Order.objects.filter(
                status__name="оплачено",
                created_at__range=[start_date, end_date]
            )
        else:
            paid_orders = Order.objects.filter(status__name="оплачено")

        total_revenue = sum(order.total_price for order in paid_orders)

        return render(request, 'orders/revenue_report.html', {
            'paid_orders': paid_orders,
            'total_revenue': total_revenue
        })

    return render(request, 'orders/revenue.html')