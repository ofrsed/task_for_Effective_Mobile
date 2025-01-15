from django.core.management.base import BaseCommand
from business_logic.models import Dish, Order, OrderItem

class Command(BaseCommand):
    help = 'Заполняем базу данных тестовыми данными'

    def handle(self, *args, **kwargs):

        dishes_data = [
            {'name': 'Пицца Маргарита', 'price': 350.00},
            {'name': 'Чай зеленый', 'price': 150.00},
            {'name': 'Пицца с ананасами', 'price': 650.00},
            {'name': 'Цезарь', 'price': 250.00},
            {'name': 'Бургер', 'price': 300.00},
            {'name': 'Салат Греческий', 'price': 450.00},
            {'name': 'Пиво', 'price': 150.00},
            {'name': 'Суп-пюре из тыквы', 'price': 120.00},
        ]

        for dish_data in dishes_data:
            Dish.objects.create(**dish_data)

        self.stdout.write(self.style.SUCCESS('Блюда добавлены!'))

        # Создание заказов
        # Получаем все блюда из базы данных
        pizza = Dish.objects.get(name='Пицца Маргарита')
        pizza2 = Dish.objects.get(name='Пицца с ананасами')
        caesar = Dish.objects.get(name='Цезарь')
        burger = Dish.objects.get(name='Бургер')

        # Создание первого заказа
        order1 = Order.objects.create(table_number=1, status='pending')

        # Добавляем блюда в заказ
        OrderItem.objects.create(order=order1, dish=pizza, quantity=2)
        OrderItem.objects.create(order=order1, dish=caesar, quantity=1)

        # Создание второго заказа
        order2 = Order.objects.create(table_number=2, status='ready')

        # Добавляем блюда в заказ
        OrderItem.objects.create(order=order2, dish=burger, quantity=3)
        OrderItem.objects.create(order=order2, dish=pizza2, quantity=1)
        OrderItem.objects.create(order=order2, dish=caesar, quantity=1)

        self.stdout.write(self.style.SUCCESS('Заказы добавлены!'))