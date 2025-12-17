from django.contrib import admin
from .models import Category, Product, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Category.

    Атрибуты:
        list_display (tuple): Поля для отображения в списке.
        search_fields (tuple): Поля для поиска.
        prepopulated_fields (dict): Автозаполнение slug на основе name.

    Методы:
        product_count(): Возвращает количество товаров в категории.
    """
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        """
        Возвращает количество товаров в категории.

        Args:
            obj (Category): Экземпляр категории.

        Returns:
            int: Количество товаров.
        """
        return Product.objects.filter(category=obj).count()
    product_count.short_description = 'Кол-во товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Product.

    Атрибуты:
        list_display (tuple): Поля для отображения в списке.
        list_filter (tuple): Поля для фильтрации.
        search_fields (tuple): Поля для поиска.
        prepopulated_fields (dict): Автозаполнение slug.
        list_editable (tuple): Поля для редактирования прямо в списке.
        readonly_fields (tuple): Только для чтения.
        fieldsets (tuple): Группировка полей в форме редактирования.

    Методы:
        get_brand(): Возвращает название бренда или 'Без бренда'.
    """
    list_display = (
        'product_name',
        'category',
        'get_brand',
        'price',
        'stock',
        'created_at')
    list_filter = ('category', 'brand', 'created_at', 'price')
    search_fields = (
        'product_name',
        'description',
        'slug',
        'category__name',
        'brand__name')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('price', 'stock')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('product_name', 'slug', 'description', 'category', 'brand')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock')
        }),
        ('Дополнительно', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_brand(self, obj):
        """
        Возвращает название бренда или строку "Без бренда".

        Args:
            obj (Product): Экземпляр товара.

        Returns:
            str: Название бренда или 'Без бренда'.
        """
        return obj.brand.name if obj.brand else "Без бренда"
    get_brand.short_description = 'Бренд'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Brand.

    Атрибуты:
        list_display (tuple): Поля для отображения в списке.
        search_fields (tuple): Поля для поиска.
        prepopulated_fields (dict): Автозаполнение slug.

    Методы:
        product_count(): Возвращает количество товаров бренда.
    """
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        """
        Возвращает количество товаров бренда.

        Args:
            obj (Brand): Экземпляр бренда.

        Returns:
            int: Количество товаров.
        """
        return Product.objects.filter(brand=obj).count()
    product_count.short_description = 'Кол-во товаров'
