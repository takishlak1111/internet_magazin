from django.shortcuts import render, get_object_or_404
from catalog.models import Product
from .models import Cart, CartItem


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session=request.session.session_key)
    return cart


def add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return render(request, 'cart/partials/cart_items.html', {'cart': cart})


def remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=get_cart(request))
    item.delete()
    return render(request, 'cart/partials/cart_items.html', {'cart': get_cart(request)})


def view(request):
    return render(request, 'cart/view.html', {'cart': get_cart(request)})