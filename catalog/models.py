from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Навзание категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name='Логотип')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        return self.products    .count()


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание продукта")
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления товара")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления товара")
    stock = models.IntegerField(default=0, verbose_name="Количество на складе")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория товаров")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, related_name='products',
                              verbose_name='Бренд')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['created_at']
        indexes = [models.Index(fields=['slug']), models.Index(fields=['price']), models.Index(fields=['created_at'])]

    def __str__(self):
        return f"{self.brand.name} {self.product_name}"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def in_stock(self):
        return self.stock > 0

    # @property
    # def average_rating(self):
    #     from reviews.models import Review
    #     reviews = Review.objects.filter(product=self)
    #     if reviews.exists():
    #         total = sum(review.rating for review in reviews)
    #         return round(total / reviews.count(), 1)
    #     return 0.0

    # @property
    # def reviews_count(self):
    #     from reviews.models import Review
    #     return Review.objects.filter(product=self).count()
