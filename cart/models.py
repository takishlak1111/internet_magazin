from django.db import models
from django.conf import settings


class Cart(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="корзина")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session = models.CharField(max_length=100, null=True, blank=True)

    def total(self):
        return sum(item.total() for item in self.items.all())  

    def item_count(self):
        return self.items.count()  

    def __str__(self):
        if self.user:
            return f"Корзина пользователя {self.user.username}"
        return f"Корзина сессии {self.session}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'