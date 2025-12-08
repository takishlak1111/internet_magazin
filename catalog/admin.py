from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return Product.objects.filter(category=obj).count()
    product_count.short_description = 'Кол-во товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # ВРЕМЕННО: убираем все методы с format_html
    list_display = ('product_name', 'category', 'get_brand', 'price', 'stock', 'created_at')
    list_filter = ('category', 'brand', 'created_at', 'price')
    search_fields = ('product_name', 'description', 'slug', 'category__name', 'brand__name')
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
        return obj.brand.name if obj.brand else "Без бренда"
    get_brand.short_description = 'Бренд'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return Product.objects.filter(brand=obj).count()
    product_count.short_description = 'Кол-во товаров'