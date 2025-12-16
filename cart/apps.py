from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Конфигурация приложения 'cart'.

    Атрибуты:
        default_auto_field (str): Тип поля для автоматического создания первичного ключа.
        name (str): Имя приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField' # поле для первичных ключей
    name = 'cart'