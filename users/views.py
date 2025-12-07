from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth 
from django.urls import reverse


from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm



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

    if request.method == 'POST': # если метод GET то формируем пустой запрос и отправлем в контекст 
        form = UserRegistrationForm(data=request.POST) # передаем словарь с данными введенными от пользователя
        if form.is_valid():
            form.save() # если форма валидна заносим пользователя в бд
            user = form.instance
            auth.login(request, user) # Если пользователь залогинился сразу регаем его 
            return HttpResponseRedirect(reverse('main:index')) # после регистрации переносим его на любую страницу (когда сделаем фронт ПЕРЕДЕЛАТЬ)
    else:  
        form = UserRegistrationForm()

    context={
        'title': 'Home - Регистрация',
        'form' : form,

    }
    return render(request,'users/registration.html',context)




@login_required # огрничваем незареганным пользователям (если нет то page not found)
def profile(request):

    if request.method == 'POST': # если метод GET то формируем пустой запрос и отправлем в контекст 
        form = ProfileForm(data=request.POST, isinstance = request.user, files=request.FILES) 
        if form.is_valid():
            form.save() 

            return HttpResponseRedirect(reverse('user:profile')) # после регистрации переносим его на лк
    else:  
        form = ProfileForm(isinstance = request.user)

    context={
        'title': 'Home - Кабинет',
        'form' : form
    }
    return render(request,'users/profile.html',context)






def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index')) ### Тоже ПЕРЕДЕЛЬ перессылку когда будет фронт 