from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Brand


def product_list(request):
    """
    Отображает список товаров с возможностью фильтрации.

    Поддерживает фильтрацию по:
        - поисковому запросу (по названию и описанию)
        - категории
        - бренду
        - цене (мин/макс)
        - наличию на складе
        - рейтингу (мин/макс)

    Args:
        request (HttpRequest): Объект запроса с возможными GET-параметрами.

    Returns:
        HttpResponse: Рендер шаблона 'catalog/product_list.html' с контекстом.
    """
    products = Product.objects.all()

    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    brand_slug = request.GET.get('brand', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    in_stock = request.GET.get('in_stock', '')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')

    if min_rating or max_rating:
        filtered_products = []
        for product in products:
            avg_rating = product.average_rating
            include = True
            if min_rating:
                try:
                    if avg_rating < float(min_rating):
                        include = False
                except (ValueError, TypeError):
                    pass
            if max_rating:
                try:
                    if avg_rating > float(max_rating):
                        include = False
                except (ValueError, TypeError):
                    pass
            if include:
                filtered_products.append(product)
        products = filtered_products

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    if in_stock:
        products = products.filter(stock__gt=0)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'current_query': query,
        'current_category': category_slug,
        'current_brand': brand_slug,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_in_stock': in_stock,
        'current_min_rating': min_rating,
        'current_max_rating': max_rating,
    }
    return render(request, 'catalog/product_list.html', context)


def category_detail(request, slug):
    """
    Отображает детальную страницу категории со списком товаров.

    Args:
        request (HttpRequest): Объект запроса.
        slug (str): URL-идентификатор категории.

    Returns:
        HttpResponse: Рендер шаблона 'catalog/category_detail.html'.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category_detail.html', context)


def product_detail(request, slug):
    """
    Отображает детальную страницу товара.

    Args:
        request (HttpRequest): Объект запроса.
        slug (str): URL-идентификатор товара.

    Returns:
        HttpResponse: Рендер шаблона 'catalog/product_detail.html'.
    """
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)