from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class UserLoginForm(AuthenticationForm):
    """
    Форма для аутентификации пользователя.

    Наследуется от стандартной AuthenticationForm с кастомизированными виджетами.

    Поля:
        username: Имя пользователя.
        password: Пароль.

    Виджеты:
        username: TextInput с классом 'form-control' и placeholder.
        password: PasswordInput с классом 'form-control' и placeholder.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.

    Наследуется от стандартной UserCreationForm с дополнительными полями
    и кастомизированными виджетами.

    Поля:
        username: Имя пользователя.
        email: Email адрес.
        password1: Пароль.
        password2: Подтверждение пароля.
        first_name: Имя (необязательно).
        last_name: Фамилия (необязательно).

    Виджеты:
        Все поля имеют кастомизированные виджеты с классами 'form-control'
        и соответствующими placeholder.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя пользователя'
        })
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу почту'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите ваш пароль'
        })
    )


class ProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.

    Поля:
        username: Имя пользователя (только для чтения).
        email: Email адрес.
        first_name: Имя.
        last_name: Фамилия.
        image: Аватар пользователя.

    Виджеты:
        username: TextInput с атрибутом readonly.
        email: EmailInput с классом 'form-control'.
        first_name: TextInput с классом 'form-control'.
        last_name: TextInput с классом 'form-control'.
        image: FileInput с классом 'form-control'.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')