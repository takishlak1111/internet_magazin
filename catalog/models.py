from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Модель категории товаров.

    Атрибуты:
        name (CharField): Название категории (макс. 100 символов).
        slug (SlugField): Уникальный URL-идентификатор категории.

    Методы:
        get_absolute_url(): Возвращает абсолютный URL для детальной страницы категории.
        __str__(): Возвращает строковое представление (название категории).
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для детальной страницы категории.

        Returns:
            str: URL вида '/category/<slug>/'.
        """
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Модель бренда.

    Атрибуты:
        name (CharField): Название бренда.
        slug (SlField): Уникальный URL-идентификатор бренда.
        description (TextField): Описание бренда (необязательно).
        logo (ImageField): Логотип бренда (необязательно).

    Свойства:
        product_count: Возвращает количество товаров бренда.

    Методы:
        get_absolute_url(): Возвращает абсолютный URL для детальной страницы бренда.
        __str__(): Возвращает название бренда.
    """
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
        """
        Возвращает абсолютный URL для детальной страницы бренда.

        Returns:
            str: URL вида '/brand/<slug>/'.
        """
        return reverse('brand_detail', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        """
        Возвращает количество товаров, связанных с брендом.

        Returns:
            int: Количество товаров бренда.
        """
        return self.products.count()


class Product(models.Model):
    """
    Модель товара.

    Атрибуты:
        product_name (CharField): Название товара.
        description (TextField): Описание товара.
        slug (SlugField): Уникальный URL-идентификатор товара.
        price (DecimalField): Цена товара.
        rating (FloatField): Рейтинг товара (по умолчанию 0.0).
        created_at (DateTimeField): Дата создания записи.
        updated_at (DateTimeField): Дата последнего обновления.
        stock (IntegerField): Количество на складе.
        category (ForeignKey): Связь с категорией.
        brand (ForeignKey): Связь с брендом (может быть пустым).

    Свойства:
        in_stock: Проверяет, есть ли товар в наличии.
        average_rating: Возвращает средний рейтинг на основе отзывов.
        reviews_count: Возвращает количество отзывов.

    Методы:
        get_absolute_url(): Возвращает абсолютный URL детальной страницы товара.
        __str__(): Возвращает строку вида "<Бренд> <Название товара>".
    """
    product_name = models.CharField(max_length=100, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание продукта")
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления товара")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления товара")
    stock = models.IntegerField(default=0, verbose_name="Количество на складе")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория товаров")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='products', verbose_name='Бренд')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f"{self.brand.name if self.brand else ''} {self.product_name}".strip()

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для детальной страницы товара.

        Returns:
            str: URL вида '/product/<slug>/'.
        """
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def in_stock(self):
        """
        Проверяет, есть ли товар в наличии.

        Returns:
            bool: True если stock > 0, иначе False.
        """
        return self.stock > 0

    @property
    def average_rating(self):
        """
        Рассчитывает средний рейтинг товара на основе отзывов.

        Returns:
            float: Средний рейтинг, округлённый до 1 знака, или 0.0 если отзывов нет.
        """
        from reviews.models import Review
        reviews = Review.objects.filter(product=self)
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0.0

    @property
    def reviews_count(self):
        """
        Возвращает количество отзывов для товара.

        Returns:
            int: Количество отзывов.
        """
        from reviews.models import Review
        return Review.objects.filter(product=self).count()