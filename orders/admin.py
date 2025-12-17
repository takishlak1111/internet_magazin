from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Встроенная админ-форма для позиций заказа.

    Атрибуты:
        model (Model): Модель OrderItem.
        extra (int): Количество дополнительных пустых форм.
        readonly_fields (list): Поля только для чтения.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Order.

    Атрибуты:
        list_display (list): Поля для отображения в списке.
        list_filter (list): Поля для фильтрации.
        search_fields (list): Поля для поиска.
        readonly_fields (list): Поля только для чтения.
        inlines (list): Встроенные формы.
        fieldsets (tuple): Группировка полей в форме редактирования.
    """
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
            'fields': ('full_name', 'email', 'phone', 'address',)
        }),
        ('Оплата', {
            'fields': ('payment', 'is_paid', 'paid_date')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели OrderItem.

    Атрибуты:
        list_display (list): Поля для отображения в списке.
        list_filter (list): Поля для фильтрации.
    """
    list_display = ['order', 'product', 'price', 'quantity', 'sum']
    list_filter = ['order__status']
