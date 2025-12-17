from django.db import models
from django.conf import settings
from django.utils import timezone


class Order(models.Model):
    """
    Модель заказа.

    Содержит информацию о заказе, клиенте, способе оплаты и статусе.

    Атрибуты:
        STATUSES (list): Доступные статусы заказа.
        PAYMENT_TYPES (list): Доступные способы оплаты.
        user (ForeignKey): Пользователь, оформивший заказ.
        cart (ForeignKey): Корзина, из которой создан заказ.
        number (CharField): Уникальный номер заказа (генерируется автоматически).
        created (DateTimeField): Дата и время создания заказа.
        status (CharField): Текущий статус заказа.
        total (DecimalField): Общая сумма заказа.
        full_name (CharField): Полное имя клиента.
        email (EmailField): Email клиента.
        phone (CharField): Телефон клиента.
        address (TextField): Адрес доставки.
        payment (CharField): Способ оплаты.
        is_paid (BooleanField): Статус оплаты.
        paid_date (DateTimeField): Дата оплаты.

    Методы:
        save(): Генерирует уникальный номер заказа при создании.
        __str__(): Возвращает строковое представление заказа.
    """
    STATUSES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('sent', 'Отправлен'),
        ('done', 'Выполнен'),
        ('canceled', 'Отменен'),
    ]

    PAYMENT_TYPES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('online', 'Онлайн'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    cart = models.ForeignKey(
        'cart.Cart',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    number = models.CharField(max_length=20, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='new')

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    payment = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES,
        default='cash')
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        """
        Возвращает строковое представление заказа.

        Returns:
            str: "Заказ #<номер заказа>".
        """
        return f'Заказ #{self.number}'

    def save(self, *args, **kwargs):
        """
        Сохраняет заказ, генерируя уникальный номер при создании.

        Номер генерируется в формате: ORDER-YYMMDD-XXXX

        Args:
            *args: Аргументы для родительского метода save.
            **kwargs: Ключевые аргументы для родительского метода save.
        """
        if not self.number:
            date_str = timezone.now().strftime('%y%m%d')
            last = Order.objects.filter(
                number__startswith=f'ORDER-{date_str}').count()
            self.number = f'ORDER-{date_str}-{last + 1:04d}'
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Модель товара в заказе.

    Связывает товар с заказом, храня цену и количество на момент покупки.

    Атрибуты:
        order (ForeignKey): Заказ, к которому относится товар.
        product (ForeignKey): Товар из каталога.
        price (DecimalField): Цена товара на момент покупки.
        quantity (PositiveIntegerField): Количество товара.

    Свойства:
        sum: Возвращает общую стоимость позиции.

    Методы:
        __str__(): Возвращает строковое представление позиции.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.PROTECT
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказе'

    def __str__(self):
        """
        Возвращает строковое представление позиции заказа.

        Returns:
            str: "<Название товара> x <количество>".
        """
        return f'{self.product.product_name} x {self.quantity}'

    @property
    def sum(self):
        """
        Рассчитывает общую стоимость позиции.

        Returns:
            Decimal: Цена умноженная на количество.
        """
        return self.price * self.quantity
