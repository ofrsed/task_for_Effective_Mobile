from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название блюда")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    id = models.AutoField(primary_key=True)
    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.dish.price * item.quantity for item in self.orderitems.all())

    def __str__(self):
        return f"Заказ {self.id} для стола {self.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE, verbose_name="Заказ")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Блюдо")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def item_total(self):
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} (заказ {self.order.id})"
