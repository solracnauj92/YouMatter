from django.contrib import admin
from .models import Item, Category, OrderModel

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(OrderModel)
