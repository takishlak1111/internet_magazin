from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session', 'item_count', 'total']

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = 'Товаров'

    def total(self, obj):
        return obj.total()

    total.short_description = 'Сумма'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'total']

    def total(self, obj):
        return obj.total()