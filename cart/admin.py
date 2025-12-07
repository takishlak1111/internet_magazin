from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['added_at', 'total_price']
    fields = ['product', 'quantity', 'total_price', 'added_at']

    def total_price(self, obj):
        return f"{obj.total_price} ₽"

    total_price.short_description = 'Сумма'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price_display', 'total_quantity_display', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_price_display', 'total_quantity_display']
    inlines = [CartItemInline]

    def total_price_display(self, obj):
        return f"{obj.total_price} ₽"

    total_price_display.short_description = 'Общая сумма'

    def total_quantity_display(self, obj):
        return obj.total_quantity

    total_quantity_display.short_description = 'Количество товаров'

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('Сводка', {
            'fields': ('total_price_display', 'total_quantity_display'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price_display', 'added_at']
    list_filter = ['added_at', 'cart__user']
    search_fields = ['product__product_name', 'cart__user__username']
    readonly_fields = ['added_at', 'total_price_display']
    list_select_related = ['cart', 'product']

    def total_price_display(self, obj):
        return f"{obj.total_price} ₽"

    total_price_display.short_description = 'Сумма'

    fieldsets = (
        ('Основная информация', {
            'fields': ('cart', 'product', 'quantity')
        }),
        ('Дополнительно', {
            'fields': ('added_at', 'total_price_display'),
            'classes': ('collapse',)
        }),
    )
