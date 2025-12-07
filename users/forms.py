from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from internet_magazin.users.models import User


class UserLoginForm(AuthenticationForm ):
    username = forms.CharField()
    password = forms.CharField()


class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model= User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password_1',
            'password_2',
        )
    
    first_name = forms.CharField(
        widget=forms.TextInput(
           attrs={
                'class':'form-control',
                'placeholder': 'Введите ваше имя'
           }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
           attrs={
                'class':'form-control',
                'placeholder': 'Введите вашу фамилию'
           }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
           attrs={
                'class':'form-control',
                'placeholder': 'Введите ваше имя пользователя'
           }
        )
    )


    email = forms.CharField(
        widget=forms.EmailInput(
           attrs={
                'class':'form-control',
                'placeholder': 'Введите вашу почту'
           }
        )
    )

    password_1 = forms.CharField(
        widget=forms.PasswordInput(
           attrs={
                'class':'form-control',
                'placeholder': 'Введите ваш пароль'
           }
        )
    )

    password_2 = forms.CharField(
        widget=forms.PasswordInput(
           attrs={
                'class':'form-control',
                'placeholder': 'Подтвердите ваш пароль'
           }
        )
    )


class ProfileForm(UserChangeForm): # чистто информация о пользователе в личном кабинете 
    model = User
    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )

    first_name = forms.ImageField()
    last_name = forms.ImageField()
    username = forms.ImageField()
    email = forms.ImageField()
