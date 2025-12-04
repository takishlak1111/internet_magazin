from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'product_count_display')
    search_fields = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}

    def product_count_display(self, obj):
        return Product.objects.filter(category=obj).count()
    product_count_display.short_description = 'Кол-во товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('product_name', 'category', 'get_brand_name', 'price', 'stock', 'in_stock_display', 'get_average_rating', 'get_reviews_count', 'is_active', 'created_at')
    list_filter = ('category', 'brand', 'is_active', 'created_at', 'price', 'get_average_rating')
    search_fields = ('product_name', 'description', 'slug', 'category_name', 'brand_name')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('price', 'stock', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'get_average_rating', 'get_reviews_count')

    fieldsets = (
        ('Основная информация', {
            'fields': ('product_name', 'slug', 'description', 'category', 'brand')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('Статистика', {
            'fields': ('get_average_rating', 'get_reviews_count')
        }),
        ('Дополнительно', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_brand_name(self, obj):
        return obj.brand.name if obj.brand else "Без бренда"
    get_brand_name.short_description = 'Бренд'

    def in_stock_display(self, obj):
        if obj.in_stock:
            return format_html('<span style="color: green;">✓ В наличии</span>')
        return format_html('<span style="color: red;">✗ Нет в наличии</span>')
    in_stock_display.short_description = 'Наличие'

    def get_average_rating(self, obj):
        return obj.average_rating
    get_average_rating.short_description = 'Средний рейтинг'

    def get_reviews_count(self, obj):
        return obj.reviews_count
    get_reviews_count.short_description = 'Кол-во отзывов'
    actions = ['activate_products', 'deactivate_products', 'set_zero_stock']

    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Активировано {updated} товаров")
    activate_products.short_description = "Активировать выбранные товары"

    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Деактивировано {updated} товаров")
    deactivate_products.short_description = "Деактивировать выбранные товары"

    def set_zero_stock(self, request, queryset):
        updated = queryset.update(stock=0)
        self.message_user(request, f"Обнулено количество у {updated} товаров")
    set_zero_stock.short_description = "Обнулить количество на складе"

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'logo_display', 'product_count_display')

    def logo_display(self, obj):
        if obj.logo:
            return format_html(f'<img src="{obj.logo.url}" width="50" height="50" />')
        return "Нет логотипа"
    logo_display.short_description = 'Логотип'

    def product_count_display(self, obj):
        return Product.objects.filter(brand=obj).count()
    product_count_display.short_description = 'Кол-во товаров'



    




