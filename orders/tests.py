from django.test import TestCase
from django.urls import reverse
from .models import Order, Item, Status
from .forms import OrderForm

class OrderFormTest(TestCase):

    def setUp(self):
        # Создаем необходимые объекты для тестов
        self.status_waiting = Status.objects.create(name="В ожидании")
        self.status_ready = Status.objects.create(name="Готово")
        self.item1 = Item.objects.create(name="Борщ", price=500)
        self.item2 = Item.objects.create(name="Пельмени", price=700)

    def test_order_create_form_valid(self):
        """Проверка корректности работы формы при валидных данных"""
        form_data = {
            'table_number': 5,
            'items': [self.item1.id, self.item2.id],
            'status': self.status_waiting.id,
            'comment': 'Тестовый комментарий',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Сохраняем форму и проверяем, что заказ был создан
        order = form.save()
        self.assertEqual(order.table_number, 5)
        self.assertEqual(order.status, self.status_waiting)
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.comment, 'Тестовый комментарий')

    def test_order_create_form_invalid(self):
        """Проверка формы с некорректными данными"""
        form_data = {
            'table_number': '',  # Пустое поле для номера стола
            'items': [self.item1.id],  # Только одно блюдо
            'status': self.status_ready.id,
            'comment': 'Неверный номер стола',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())  # Форма не должна быть валидной
        self.assertEqual(len(form.errors), 1)  # Ожидаем одну ошибку (для номера стола)

    def test_order_update_form(self):
        """Проверка формы редактирования заказа"""
        # Создаем заказ для редактирования
        order = Order.objects.create(
            table_number=10,
            status=self.status_waiting,
            comment="Первоначальный комментарий"
        )
        order.items.add(self.item1, self.item2)

        # Данные для обновления
        form_data = {
            'table_number': 12,
            'items': [self.item1.id],
            'status': self.status_ready.id,
            'comment': 'Обновленный комментарий',
        }
        form = OrderForm(data=form_data, instance=order)
        self.assertTrue(form.is_valid())

        # Сохраняем обновленный заказ
        order = form.save()
        self.assertEqual(order.table_number, 12)
        self.assertEqual(order.status, self.status_ready)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.comment, 'Обновленный комментарий')

    def test_order_create_view(self):
        """Проверка представления для создания заказа"""
        url = reverse('order_create')
        data = {
            'table_number': 5,
            'items': [self.item1.id, self.item2.id],
            'status': self.status_waiting.id,
            'comment': 'Комментарий для заказа'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после успешного создания

        # Проверяем, что заказ был создан в базе данных
        order = Order.objects.last()
        self.assertEqual(order.table_number, 5)
        self.assertEqual(order.status, self.status_waiting)

    def test_order_list_view(self):
        """Проверка представления списка заказов"""
        url = reverse('order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertContains(response, "Список заказов")  # Проверяем наличие нужного текста на странице
from django.test import TestCase

# Create your tests here.
