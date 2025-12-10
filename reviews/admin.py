from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['text', 'user__username', 'product__name']
    readonly_fields = ['created_at']
    list_per_page = 20

    fieldsets = (
        ('Основное', {
            'fields': ('product', 'user', 'rating', 'text')
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )