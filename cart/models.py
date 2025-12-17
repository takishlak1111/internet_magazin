from django.db import models
from django.conf import settings


class Cart(models.Model):
    """
    Модель корзины покупок.

    Корзина может быть привязана к пользователю (если авторизован)
    или к сессии (для неавторизованных пользователей).

    Атрибуты:
        name (CharField): Название корзины (необязательное).
        user (OneToOneField): Связь с пользователем (может быть None).
        session (CharField): Идентификатор сессии (может быть None).

    Методы:
        total(): Возвращает общую стоимость всех товаров в корзине.
        item_count(): Возвращает количество позиций в корзине.
        __str__(): Возвращает строковое представление корзины.
    """
    name = models.CharField(max_length=100, blank=True, verbose_name="корзина")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    session = models.CharField(max_length=100, null=True, blank=True)

    def total(self):
        """
        Рассчитывает общую стоимость всех товаров в корзине.

        Returns:
            float: Сумма стоимости всех товаров с учетом количества.
        """
        return sum(item.total() for item in self.items.all())

    def item_count(self):
        """
        Возвращает количество позиций в корзине.

        Returns:
            int: Количество уникальных товаров в корзине.
        """
        return self.items.count()

    def __str__(self):
        """
        Возвращает строковое представление корзины.

        Returns:
            str: "Корзина пользователя <username>" или "Корзина сессии <session_id>".
        """
        if self.user:
            return f"Корзина пользователя {self.user.username}"
        return f"Корзина сессии {self.session}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """
    Модель элемента корзины (товар с количеством).

    Связывает товар с корзиной и хранит количество.

    Атрибуты:
        cart (ForeignKey): Связь с корзиной.
        product (ForeignKey): Связь с товаром из каталога.
        quantity (IntegerField): Количество товара (по умолчанию 1).

    Методы:
        total(): Возвращает стоимость позиции (цена * количество).
        __str__(): Возвращает строковое представление элемента.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items')  # related_name нужн для быстрого обращения
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total(self):
        """
        Рассчитывает стоимость позиции.

        Returns:
            Decimal: Стоимость товара умноженная на количество.
        """
        return self.product.price * self.quantity

    def __str__(self):
        """
        Возвращает строковое представление элемента корзины.

        Returns:
            str: "<Название товара> x <количество>".
        """
        return f"{self.product.product_name} x {self.quantity}"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
