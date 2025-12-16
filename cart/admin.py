from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Cart.

    Атрибуты:
        list_display (list): Поля для отображения в списке.
        list_filter (list): Поля для фильтрации.
        search_fields (list): Поля для поиска.

    Методы:
        item_count(): Возвращает количество товаров в корзине.
        total(): Возвращает общую стоимость корзины.
    """
    list_display = ['id', 'user', 'session', 'item_count', 'total']
    list_filter = ['user']

    def item_count(self, obj):
        """
        Возвращает количество товаров в корзине.

        Args:
            obj (Cart): Экземпляр корзины.

        Returns:
            int: Количество товаров.
        """
        return obj.items.count()

    item_count.short_description = 'Товаров' # просто назыание в админке

    def total(self, obj):
        """
        Возвращает общую стоимость корзины.

        Args:
            obj (Cart): Экземпляр корзины.

        Returns:
            Decimal: Общая стоимость.
        """
        return obj.total()

    total.short_description = 'Сумма'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели CartItem.

    Атрибуты:
        list_display (list): Поля для отображения в списке.
        list_filter (list): Поля для фильтрации.
        search_fields (list): Поля для поиска.

    Методы:
        total(): Возвращает стоимость позиции.
    """
    list_display = ['product', 'cart', 'quantity', 'total']
    list_filter = ['cart__user']

    def total(self, obj):
        """
        Возвращает стоимость позиции.

        Args:
            obj (CartItem): Экземпляр элемента корзины.

        Returns:
            Decimal: Стоимость товара с учетом количества.
        """
        return obj.total()

    total.short_description = 'Сумма' # названия поля в бд