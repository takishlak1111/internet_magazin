from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session', 'item_count', 'total']
    list_filter = ['user']
    search_fields = ['user__username', 'session']

    def item_count(self, obj):
        return obj.items.count()  # Используем items
    
    item_count.short_description = 'Товаров'

    def total(self, obj):
        return obj.total()
    
    total.short_description = 'Сумма'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'total']
    list_filter = ['cart__user']
    search_fields = ['product__name', 'cart__user__username']

    def total(self, obj):
        return obj.total()
    
    total.short_description = 'Сумма'