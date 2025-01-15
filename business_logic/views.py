from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.defaults import page_not_found

menu = ['О сайте', 'Заказы', 'Выручка']



def index(request):
    data = {'title': 'Кафе'}
    return render(request, 'business_logic/index.html', data)

from .models import Dish, Order, OrderItem

def get_all_dishes(request):
    dishes = Dish.objects.all().values('id', 'name', 'price')
    data = list(dishes)
    return JsonResponse(data, safe=False)


def get_order_with_details(request, order_id):
    try:
        order = Order.objects.prefetch_related('orderitems__dish').get(id=order_id)
        items = [
            {
                "dish": item.dish.name,
                "quantity": item.quantity,
                "price_per_item": item.dish.price,
                "item_total": item.item_total()
            }
            for item in order.orderitems.all()
        ]

        data = {
            "id": order.id,
            "table_number": order.table_number,
            "status": order.get_status_display(),
            "created_at": order.created_at,
            "total_price": order.total_price(),
            "items": items
        }
        return JsonResponse(data, safe=False)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

from django.db.models import Sum, F


def calculate_total_revenue(request):
    total_revenue = Order.objects.filter(status='paid').annotate(
        revenue=Sum(F('orderitems__dish__price') * F('orderitems__quantity'))
    ).aggregate(total=Sum('revenue'))['total']

    return JsonResponse({"total_revenue": total_revenue or 0}, safe=False)