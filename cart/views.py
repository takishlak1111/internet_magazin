from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from catalog.models import Product
from .models import Cart, CartItem


def get_cart(request):
    """
    Возвращает корзину для текущего пользователя или сессии.

    Если пользователь авторизован - возвращает корзину пользователя.
    Если не авторизован - возвращает корзину по ключу сессии.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        Cart: Объект корзины.
    """
    if request.user.is_authenticated:
        # гет он креате может создать новую корзину если нету (возвращает
        # кортеж и 2 объектов, второй это просто будево создан не создан)
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # если нету ключа сесси то создаем
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session=session_key)
    return cart


@require_POST
def add(request, product_id):
    """
    Добавляет товар в корзину.

    Поддерживает AJAX-запросы и обычные POST-запросы.
    Проверяет наличие товара на складе.

    Args:
        request (HttpRequest): Объект запроса.
        product_id (int): ID товара для добавления.

    Returns:
        JsonResponse: Для AJAX-запросов.
        HttpResponseRedirect: Для обычных запросов.
    """
    try:
        cart = get_cart(request)
        product = get_object_or_404(Product, id=product_id)

        quantity = int(request.POST.get('quantity', 1))

        if not product.in_stock:
            message = "Товар отсутствует на складе"
        elif product.stock < quantity:
            message = f"Недостаточно товара. Доступно: {product.stock} шт."
        else:
            item, created = CartItem.objects.get_or_create(
                cart=cart, product=product)
            if not created:  # проверка на был ли товар в корзине
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()

            # проверяем в заголвке (request.headers) методом get(получаем) ajax
            # ли это запрос
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'cart_count': cart.items.count(),
                    'total': float(cart.total()),
                    # JS получает этот json обновляет счетчик корзины и
                    # показывает сообщение
                    'message': f'Товар "{product.product_name}" добавлен в корзину'
                })

            return redirect('catalog:product_detail', product_id=product_id)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': message
            })

        return redirect('catalog:product_detail', product_id=product_id)

    except Exception as e:
        print(f"Ошибка при добавлении в корзину: {e}")  # в консоль сервера
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Ошибка сервера: {str(e)}'
            })
        return redirect('catalog:product_list')


def remove(request, item_id):
    """
    Удаляет товар из корзины.

    Args:
        request (HttpRequest): Объект запроса.
        item_id (int): ID элемента корзины для удаления.

    Returns:
        JsonResponse: Для AJAX-запросов.
        HttpResponseRedirect: Для обычных запросов.
    """
    try:
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.items.count(),
                'total': float(cart.total()),
                'message': 'Товар удален из корзины'
            })

        return redirect('cart:view')
    except Exception as e:
        print(f"Ошибка при удалении из корзины: {e}")
        return redirect('cart:view')


def view(request):
    """
    Отображает содержимое корзины.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Рендер шаблона cart/view.html с данными корзины.
    """
    cart = get_cart(request)
    cart_items = cart.items.all()
    return render(request, 'cart/view.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.total()
    })
