from django.db import models

class Category(models.Model):

    name = models.CharField(max_length = 100, verbose_name = "Навзание категории")
    description = models.TextField( max_length = 100, blank = True, verbose_name = "Описание категории")

    class Meta:

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):

        return self.name

class Product(models.Model):

    product_name = models.CharField(max_length = 100, verbose_name = "Название продукта")
    description = models.TextField(verbose_name = "Описание продукта")
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Цена")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = "Категория товаров")
    rating = models.FloatField(default = 0.0,  verbose_name = "Рейтинг товара")
    crated_at = models.DateTimeField(auto_now_add = True, verbose_name = "Дата добавления товара")
    updated_at = models.DateTimeField(auto_now = True, verbose_name = "Дата обновленияь товара")

    class Meta:

        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} - {self.price} руб."



