from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.core.validators import MinValueValidator

class ProductManager(models.Manager):

    def search(self, query):
        if not query:
            return self.get_queryset()

        return self.get_queryset().filter(
            models.Q(product_name__icontains=query) |
            models.Q(description__icontains=query)
        )

    def filter_by_category(self, category_slug):
        if not category_slug:
            return self.get_queryset()

        return self.get_queryset().filter(category__slug=category_slug)

    def filter_by_brand(self, brand_slug):
        if not brand_slug:
            return self.get_queryset()

        return self.get_queryset().filter(brand__slug=brand_slug)

    def filter_by_price(self, min_price=None, max_price=None):
        queryset = self.get_queryset()

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def filter_in_stock(self, in_stock_only):
        if in_stock_only:
            return self.get_queryset().filter(stock__gt=0)
        return self.get_queryset()

    def apply_filters(self, filters):
        queryset = self.get_queryset()

        if 'q' in filters:
            queryset = queryset.search(filters['q'])

        if 'category' in filters:
            queryset = queryset.filter_by_category(filters['category'])

        if 'brand' in filters:
            queryset = queryset.filter_by_brand(filters['brand'])

        if 'min_price' in filters:
            queryset = queryset.filter_by_price(min_price=filters['min_price'])

        if 'max_price' in filters:
            queryset = queryset.filter_by_price(max_price=filters['max_price'])

        if 'in_stock' in filters:
            queryset = queryset.filter_in_stock(filters['in_stock'])

        return queryset


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
        return self.objects.count()


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

    objects = ProductManager()

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
