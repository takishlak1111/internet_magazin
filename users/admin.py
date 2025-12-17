from django.contrib import admin
from users.models import User


admin.site.register(User)
"""
Регистрация модели User в админ-панели.

Использует стандартную регистрацию без кастомизации.
Для кастомизации админ-панели можно создать класс UserAdmin.
"""
