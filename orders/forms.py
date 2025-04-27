from django import forms
from .models import Order, Status, Item

class OrderForm(forms.ModelForm):
    # Поле для выбора блюд
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status', 'comment']
        widgets = {
            'items': forms.CheckboxSelectMultiple(),  # Для отображения мультивыбора (чекбоксы)
        }

# Форма для обновления статуса заказа
class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
