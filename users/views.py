from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from cart.models import Cart, CartItem
from .forms import ProfileForm, UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
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
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth_login(request, user)
            return HttpResponseRedirect(reverse('catalog:product_list'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    user = request.user
    
    
    cart, created = Cart.objects.get_or_create(user=user)
    
    
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = cart.total() if cart_items.exists() else 0
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
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
    auth_logout(request)
    return redirect(reverse('catalog:product_list'))