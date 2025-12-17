from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказа.

    Поля:
        full_name: Полное имя клиента.
        email: Email клиента.
        phone: Телефон клиента.
        address: Адрес доставки.
        payment: Способ оплаты.

    Виджеты:
        address: Textarea с 3 строками.

    Методы:
        __init__(): Инициализирует форму, подставляя данные пользователя.
    """
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму с подстановкой данных пользователя.

        Если пользователь авторизован, автоматически заполняет email.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Ключевые аргументы.
        """
        super().__init__(*args, **kwargs)
        if 'initial' not in kwargs and 'instance' not in kwargs:
            user = self.user if hasattr(self, 'user') else None
            if user and user.is_authenticated:
                self.fields['email'].initial = user.email
