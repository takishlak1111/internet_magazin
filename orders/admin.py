from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'user', 'total', 'status', 'created', 'is_paid']
    list_filter = ['status', 'is_paid', 'payment', 'created']
    search_fields = ['number', 'user__username', 'email', 'phone']
    readonly_fields = ['number', 'created', 'total']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Основное', {
            'fields': ('number', 'user', 'status', 'total', 'created')
        }),
        ('Данные клиента', {
            'fields': ('full_name', 'email', 'phone', 'address', )
        }),
        ('Оплата', {
            'fields': ('payment', 'is_paid', 'paid_date')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'sum']
    list_filter = ['order__status']