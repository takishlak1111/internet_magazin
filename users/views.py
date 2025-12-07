from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth 
from django.urls import reverse

from users.forms import UserLoginForm



def login(request):

    if request.method == 'POST': # если метод GET то формируем пустой запрос и отправлем в контекст 
        form = UserLoginForm(data=request.POST) # передаем словарь с данными введенными от пользователя
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # проверяет есть ли такой пользователь в бд
            if user:
                auth.login(request, user) # если пользователь есть мы его авторизуем 
                return HttpResponseRedirect(reverse('main:index')) # после регистрации переносим его на главную(любую) страницу
    else:  
        form = UserLoginForm()

    context={
        'title': 'Home - Авторизация',
        'form' : form,
    }
    return render(request,'users/login.html',context)



def registration(request):
    context={
        'title': 'Home - Регистрация'
    }
    return render(request,'users/registration.html',context)



def profile(request):
    context={
        'title': 'Home - Кабинет'
    }
    return render(request,'users/profile.html',context)



def logout(request):
    context={
        'title': 'Home - Авторизация'
    }
    return render(request,'',context)