from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения 'users'.

    Атрибуты:
        default_auto_field (str): Тип поля для автоматического создания первичного ключа.
        name (str): Имя приложения.
        verbose_name (str): Человекочитаемое имя приложения для админ-панели.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'пользователь'