from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Форма для создания и редактирования отзыва.

    Поля:
        rating: Оценка от 1 до 5 звезд.
        text: Текстовый отзыв.

    Виджеты:
        rating: Select с вариантами от 1 до 5.
        text: Textarea с 3 строками и placeholder.
    """
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i}') for i in range(1, 6)]), # селект - выпадающий список
            'text': forms.Textarea(attrs={
                'rows': 3, # просто высота строки
                'placeholder': 'Ваш отзыв...',
                'class': 'form-control'
            }),
        }