from django.db import models
from django.conf import settings
from django.core.cache import cache
from catalog.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-updated_at']

    def __str__(self):
        return f'Корзина {self.user.email}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def add_product(self, product, quantity=1, override_quantity=False):
        item, created = CartItem.objects.get_or_create(cart=self, product=product, defaults={'quantity': quantity})
        if not created:
            if override_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity
            item.save()
        self.updated_at = models.DateTimeField(auto_now=True)
        self.save(update_fields=['updated_at'])
        return item

    def remove_product(self, product):
        self.items.filter(product=product).delete()
        self.updated_at = models.DateTimeField(auto_now=True)
        self.save(update_fields=['updated_at'])

    def clear(self):
        self.items.all().delete()
        self.updated_at = models.DateTimeField(auto_now=True)
        self.save(update_fields=['updated_at'])

    def update_quantity(self, product, quantity):
        if quantity > 0:
            self.add_product(product, quantity, override_quantity=True)
        else:
            self.remove_product(product)

    def merge_with_session_cart(self, session_cart_data):
        for product_id_str, quantity in session_cart_data.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                self.add_product(product, quantity)
            except (Product.DoesNotExist, ValueError):
                continue

    @property
    def items_list(self):
        return [{'product': item.product, 'quantity': item.quantity, 'total_price': item.total_price, 'is_available': item.product.stock >= item.quantity} \
                for item in self.items.select_related('product').all()]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ['cart', 'product']
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.product.product_name} × {self.quantity}'

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def is_available(self):
        return self.product.stock >= self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.updated_at = models.DateTimeField(auto_now=True)
        self.cart.save(update_fields=['updated_at'])


class SessionCart:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        if 'cart' not in self.session:
            self.session['cart'] = {}

        self._cart_data = self.session['cart']

    def __len__(self):
        return len(self._cart_data)

    @property
    def total_quantity(self):
        return sum(self._cart_data.values())

    @property
    def total_price(self):
        total = 0
        for product_id_str, quantity in self._cart_data.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                total += product.price * quantity
            except (Product.DoesNotExist, ValueError):
                continue
        return total

    @property
    def items(self):
        items = []
        for product_id_str, quantity in self._cart_data.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity,'is_available': product.stock >= quantity})
            except (Product.DoesNotExist, ValueError):
                continue
        return items

    @property
    def items_list(self):
        return self.items

    def add(self, product_id, quantity=1, override_quantity=False):
        product_id_str = str(product_id)

        if product_id_str in self._cart_data:
            if override_quantity:
                self._cart_data[product_id_str] = quantity
            else:
                self._cart_data[product_id_str] += quantity
        else:
            self._cart_data[product_id_str] = quantity

        self._save()

    def remove(self, product_id):
        product_id_str = str(product_id)
        if product_id_str in self._cart_data:
            del self._cart_data[product_id_str]
            self._save()

    def clear(self):
        self._cart_data.clear()
        self._save()

    def update_quantity(self, product_id, quantity):
        if quantity > 0:
            self.add(product_id, quantity, override_quantity=True)
        else:
            self.remove(product_id)

    def get_quantity(self, product_id):
        return self._cart_data.get(str(product_id), 0)

    def _save(self):
        self.session['cart'] = self._cart_data
        self.session.modified = True

    def convert_to_user_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)

        for product_id_str, quantity in self._cart_data.items():
            try:
                product = Product.objects.get(id=int(product_id_str))
                cart.add_product(product, quantity)
            except (Product.DoesNotExist, ValueError):
                continue
        self.clear()
        return cart

    def __str__(self):
        return f'Сессионная корзина ({self.total_quantity} товаров)'