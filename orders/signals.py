from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order

@receiver(m2m_changed, sender=Order.items.through)
def update_total_price(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        total = sum(item.price for item in instance.items.all())
        instance.total_price = total
        instance.save()
