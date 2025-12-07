from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['added_at', 'total_price', 'is_available']
    fields = ['product', 'quantity', 'total_price', 'is_available', 'added_at']


    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Сумма'

    def is_available(self, obj):
        return obj.is_available

    is_available.short_description = 'В наличии'
    is_available.boolean = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_price', 'get_total_quantity', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price', 'get_total_quantity']
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return f"{obj.total_price} ₽"

    get_total_price.short_description = 'Общая сумма'
    get_total_price.admin_order_field = 'total_price'

    def get_total_quantity(self, obj):
        return obj.total_quantity

    get_total_quantity.short_description = 'Количество товаров'

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('Сводка', {
            'fields': ('get_total_price', 'get_total_quantity'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_total_price', 'added_at', 'is_available']
    list_filter = ['added_at', 'cart__user']
    search_fields = ['product__product_name', 'cart__user__username']
    readonly_fields = ['added_at', 'get_total_price', 'is_available']
    list_select_related = ['cart', 'product']

    def get_total_price(self, obj):
        return obj.total_price

    get_total_price.short_description = 'Сумма'

    def is_available(self, obj):
        return obj.is_available

    is_available.short_description = 'В наличии'
    is_available.boolean = True

    fieldsets = (
        ('Основная информация', {
            'fields': ('cart', 'product', 'quantity')
        }),
        ('Дополнительно', {
            'fields': ('added_at', 'get_total_price', 'is_available'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.quantity > obj.product.stock:
            from django.contrib import messages
            messages.warning(
                request,
                f'Внимание! Заказано {obj.quantity} шт., а в наличии только {obj.product.stock} шт.'
            )
        super().save_model(request, obj, form, change)