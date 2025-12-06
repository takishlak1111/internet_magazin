from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from catalog.models import Product
from .models import Cart, SessionCart


def get_cart_for_request(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        return SessionCart(request)


def cart_detail(request):
    cart = get_cart_for_request(request)

    context = {'cart': cart, 'items': cart.items_list, 'total_price': cart.total_price, 'total_quantity': cart.total_quantity,}

    return render(request, 'cart/cart_detail.html', context)


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = get_cart_for_request(request)

    if isinstance(cart, Cart):
        cart.add_product(product, quantity)
    else:
        cart.add(product_id, quantity)

    messages.success(request,f'"{product.product_name}" добавлен в корзину')

    referer = request.META.get('HTTP_REFERER', product.get_absolute_url())
    return redirect(referer)


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = get_cart_for_request(request)

    if isinstance(cart, Cart):
        cart.remove_product(product)
    else:
        cart.remove(product_id)

    messages.success(request,f'"{product.product_name}" удалён из корзины')

    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = get_cart_for_request(request)

    if isinstance(cart, Cart):
        cart.update_quantity(product, quantity)
    else:
        cart.update_quantity(product_id, quantity)

    messages.success(request, f'Количество "{product.product_name}" обновлено')

    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    cart = get_cart_for_request(request)
    cart.clear()

    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart_detail')