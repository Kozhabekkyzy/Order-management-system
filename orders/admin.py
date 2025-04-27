from django.contrib import admin
from .models import Order, Status, Item

admin.site.register(Order)
admin.site.register(Status)
admin.site.register(Item)


# Register your models here.
