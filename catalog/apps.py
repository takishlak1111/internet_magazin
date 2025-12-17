from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """
    Конфигурация приложения 'catalog'.

    Атрибуты:
        default_auto_field (str): Тип поля для автоматического создания первичного ключа.
        name (str): Имя приложения.
        verbose_name (str): Человекочитаемое имя приложения для админ-панели.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = 'Каталог товаров'
