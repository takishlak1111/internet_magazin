from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import OrderForm


@login_required
def create_order(request):
    """
    Создает заказ из корзины пользователя.

    Проверяет:
        - Наличие товаров в корзине.
        - Достаточность товаров на складе.

    В случае успеха:
        - Создает заказ.
        - Создает позиции заказа.
        - Уменьшает остатки на складе.
        - Очищает корзину.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Страница создания заказа или редирект.
    """
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items.exists():
        messages.warning(request, 'Корзина пуста')
        return redirect('cart:detail')

    for item in items:
        if item.quantity > item.product.stock:
            messages.error(request, f'Недостаточно товара: {item.product.product_name}')
            return redirect('cart:detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.cart = cart
                    order.total = cart.total()
                    order.save()

                    for item in items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            price=item.product.price,
                            quantity=item.quantity
                        )

                        item.product.stock -= item.quantity
                        item.product.save()

                    items.delete()

                    messages.success(request, f'Заказ #{order.number} создан!')
                    return redirect('orders:detail', order_id=order.id)

            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
    else:
        initial = {}
        if request.user.first_name and request.user.last_name:
            initial['full_name'] = f'{request.user.first_name} {request.user.last_name}'
        elif request.user.username:
            initial['full_name'] = request.user.username

        if request.user.email:
            initial['email'] = request.user.email

        form = OrderForm(initial=initial)
        form.user = request.user

    context = {
        'form': form,
        'cart': cart,
        'items': items,
    }
    return render(request, 'orders/create.html', context)


@login_required
def order_list(request):
    """
    Отображает список заказов текущего пользователя.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Страница со списком заказов.
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Отображает детальную информацию о заказе.

    Примечание: В текущей реализации происходит редирект на список товаров.
    Нужно доработать для отображения деталей заказа.

    Args:
        request (HttpRequest): Объект запроса.
        order_id (int): ID заказа.

    Returns:
        HttpResponseRedirect: Редирект на список товаров.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})