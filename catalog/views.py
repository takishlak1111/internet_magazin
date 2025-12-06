from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Brand


def product_list(request):
    """Главная страница каталога - все товары"""
    products = Product.objects.filter()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, slug):
    """Страница одного товара"""
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})


def category_detail(request, slug):
    """Товары в категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products
    })


def brand_detail(request, slug):
    """Товары бренда"""
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand)
    return render(request, 'catalog/brand_detail.html', {
        'brand': brand,
        'products': products
    })


def product_search(request):
    """Поиск товаров"""
    query = request.GET.get('q', '')
    products = Product.objects.filter()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        )

    return render(request, 'catalog/product_search.html', {
        'products': products,
        'query': query
    })
