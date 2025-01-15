from django.contrib import admin
from django.urls import path, include

from . import views
from .consumers import OrderConsumer

from .views import get_all_dishes, get_order_with_details,calculate_total_revenue, index

urlpatterns = [
    path('', index, name='index'),
    path('api/dishes/', get_all_dishes, name='get_all_dishes'),
    path('api/orders/<int:order_id>/', get_order_with_details, name='get_order_with_details'),
    path('api/revenue/', calculate_total_revenue, name='calculate_total_revenue'),
]

