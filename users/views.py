from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # тут чтобы не ругалось на фунции(одно имя)
from django.urls import reverse
from cart.models import Cart, CartItem
from .forms import ProfileForm, UserLoginForm, UserRegistrationForm


def login(request):
<<<<<<< HEAD
    """
    Обрабатывает аутентификацию пользователя.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Страница входа или редирект на главную при успешной аутентификации.
    """
    if request.method == 'POST':
=======
    if request.method == 'POST': # Post - чисто данные формы 
>>>>>>> a09abf6e971940624d1cd7c4ed88851f911fdd37
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password) # ищем пароль и юз в бд
            if user:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('catalog:product_list'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    """
    Обрабатывает регистрацию нового пользователя.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Страница регистрации или редирект на главную при успешной регистрации.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance # доступ к созданной форме
            auth_login(request, user)
            return HttpResponseRedirect(reverse('catalog:product_list'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@login_required # декоратор для проверки вошел ли пользователь чтобы смотреть защищенные стр
def profile(request):
    """
    Отображает и обрабатывает редактирование профиля пользователя.

    Также отображает информацию о корзине пользователя.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Страница профиля пользователя.
    """
    user = request.user
<<<<<<< HEAD

    cart, created = Cart.objects.get_or_create(user=user)

=======
    
    
    cart, created = Cart.objects.get_or_create(user=user) # ищет корзину или создает ее
    #try:
        #cart = Cart.objects.get(user=user)  # Пытаемся найти
        #created = False
    #except Cart.DoesNotExist:  # Если не нашли
        #cart = Cart.objects.create(user=user)  # Создаем
        #created = True
    
>>>>>>> a09abf6e971940624d1cd7c4ed88851f911fdd37
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = cart.total() if cart_items.exists() else 0

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
        else: # выдаем по какому полю какая ошибка
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else: # это если get запрос(получение данных)
        form = ProfileForm(instance=user)

    context = {
        'title': 'Home - Кабинет',
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user': user,
    }

    return render(request, 'users/profile.html', context)


def logout(request):
    """
    Выполняет выход пользователя из системы.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponseRedirect: Редирект на главную страницу каталога.
    """
    auth_logout(request)
    return redirect(reverse('catalog:product_list'))