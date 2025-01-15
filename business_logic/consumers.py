import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Order, OrderItem, Dish
from asgiref.sync import sync_to_async

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "WebSocket connection established."
        }))



    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        # Получение всех заказов
        if action == "get-orders":
            orders = await self.get_orders()
            await self.send(text_data=json.dumps({
                "action": "get-orders",
                "orders": orders
            }))
        elif action == "get-dishes":
            dishes = await self.get_dishes()
            await self.send(text_data=json.dumps({
                "action": "get-dishes",
                "dishes": dishes
            }))

        elif action == "add-order":
            data = data.get('order')
            table_number = data.get("table_number")
            items = data.get("items")
            order = await self.create_order(table_number, items)
            orders = await self.get_orders()
            await self.send(text_data=json.dumps({
                "action": "get-orders",
                "orders": orders
            }))
        elif action == "change-status":
            order_id = data.get('order_id')
            status = data.get('status')

            order = await self.change_order_status(order_id, status)

            orders = await self.get_orders()
            await self.send(text_data=json.dumps({
                "action": "get-orders",
                "orders": orders
            }))


        elif action == "delete-order":
            order_id = data.get('order_id')
            order = await self.delete_order_by_id(order_id)

            orders = await self.get_orders()
            await self.send(text_data=json.dumps({
                "action": "get-orders",
                "orders": orders
            }))

        else:
            await self.send(text_data=json.dumps({
                "error": "Unknown action."
            }))

    @sync_to_async
    def get_orders(self):
        orders = Order.objects.all().order_by('id')

        status_translate = {'pending': 'В ожидании',
                            'ready': 'Готово',
                            'paid': 'Оплачено'}



        orders_data = []
        for order in orders:
            order_items = []
            for item in order.orderitems.all():
                order_items.append({
                    "dish": item.dish.name,
                    "price": str(item.dish.price),
                    "quantity": item.quantity,
                    "total": str(item.item_total())
                })

            order_data = {
                "id": order.id,
                "table_number": order.table_number,
                "items": order_items,
                "total_price": str(order.total_price()),
                "status": status_translate.get(order.status)
            }

            orders_data.append(order_data)
        return orders_data

    @sync_to_async
    def create_order(self, order_name, items):

        table_number = order_name
        items = items

        order = Order.objects.create(table_number=table_number)

        for item in items:
            dish_name = item.get('dish')
            quantity = item.get('quantity')

            try:
                dish = Dish.objects.get(name=dish_name)
            except Dish.DoesNotExist:
                raise ValueError(f"Блюдо с именем {dish_name} не найдено")

            OrderItem.objects.create(order=order, dish=dish, quantity=quantity)

        return order

    @sync_to_async
    def delete_order_by_id(self, order_id):
        order = Order.objects.get(id=order_id)
        order.orderitems.all().delete()
        order.delete()
        return True


    @sync_to_async
    def get_dishes(self):
        dishes = Dish.objects.all()
        dishes_data = []
        for dish in dishes:
            dishes_data.append({
                "id": dish.id,
                "name": dish.name,
                "price": str(dish.price),
            })
        return dishes_data


    @sync_to_async
    def change_order_status(data, order_id, status):
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        return {"success": f"Order {order_id} status updated to {status}"}
