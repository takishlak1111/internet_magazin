from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from catalog.models import Product


class Review(models.Model):
    """
    Модель отзыва на товар.

    Содержит оценку и текстовый отзыв пользователя на конкретный товар.
    Каждый пользователь может оставить только один отзыв на товар.

    Атрибуты:
        product (ForeignKey): Товар, к которому относится отзыв.
        user (ForeignKey): Пользователь, оставивший отзыв.
        rating (IntegerField): Оценка от 1 до 5 звезд.
        text (TextField): Текстовый отзыв (необязательный).
        created_at (DateTimeField): Дата и время создания отзыва.

    Методы:
        __str__(): Возвращает строковое представление отзыва.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, # при удалении удаляются все отзывы
        related_name='reviews',
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']  # сортировка по убыванию даты

    def __str__(self):
        """
        Возвращает строковое представление отзыва.

        Returns:
            str: "<Пользователь> - <Товар> (<Рейтинг>⭐)".
        """
        return f'{self.user} - {self.product} ({self.rating}⭐)'