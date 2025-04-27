from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.name} - {self.price}₸"


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    table_number = models.PositiveIntegerField()
    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

def save(self, *args, **kwargs):
    if not self.total_price or self.total_price == 0:
        self.total_price = sum(item.price for item in self.items.all())
    super().save(*args, **kwargs)

    def __str__(self):
        return f"Стол {self.table_number} | Статус: {self.status.name} | Цена: {self.total_price}₸"
