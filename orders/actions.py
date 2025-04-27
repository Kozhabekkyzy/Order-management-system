def order_total_price(order):
    total = sum(item.price for item in order.items.all())
    order.total_price = total
    order.save()
