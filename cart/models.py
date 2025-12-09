from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session = models.CharField(max_length=100, null=True, blank=True)

    def total(self):
        return sum(item.total() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity