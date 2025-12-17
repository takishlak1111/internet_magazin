from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную AbstractUser.

    Добавляет поле для изображения пользователя (аватара).

    Атрибуты:
        image (ImageField): Изображение пользователя (аватар), сохраняется в 'users_images/'.

    Методы:
        __str__(): Возвращает строковое представление пользователя (username).
    """
    image = models.ImageField(upload_to='users_images', blank=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        Returns:
            str: Имя пользователя (username).
        """
        return self.username
