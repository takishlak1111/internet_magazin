from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Конфигурация приложения 'reviews'.

    Атрибуты:
        default_auto_field (str): Тип поля для автоматического создания первичного ключа.
        name (str): Имя приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
