import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import tempfile
import shutil
import os

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для модели User"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_model_meta(self):
        """Тест метаданных модели"""
        self.assertEqual(User._meta.db_table, 'user')
        self.assertEqual(User._meta.verbose_name, 'Пользователь')
        self.assertEqual(User._meta.verbose_name_plural, 'Пользователи')
    
    def test_user_image_field(self):
        """Тест поля изображения"""
        self.assertTrue(hasattr(self.user, 'image'))
        self.assertIsNone(self.user.image)


class UserFormsTest(TestCase):
    """Тесты для форм пользователя"""
    
    def test_login_form_valid(self):
        """Тест валидной формы логина"""
        from .forms import UserLoginForm
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_login_form_invalid(self):
        """Тест невалидной формы логина"""
        from .forms import UserLoginForm
        form_data = {
            'username': '',
            'password': ''
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
    
    def test_registration_form_valid(self):
        """Тест валидной формы регистрации"""
        from .forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_password_mismatch(self):
        """Тест формы регистрации с несовпадающими паролями"""
        from .forms import UserRegistrationForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'differentpass',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_profile_form_valid(self):
        """Тест валидной формы профиля"""
        from .forms import ProfileForm
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'testuser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        form = ProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
    
    def test_profile_form_username_readonly(self):
        """Тест что поле username только для чтения в форме профиля"""
        from .forms import ProfileForm
        form = ProfileForm()
        self.assertEqual(form.fields['username'].widget.attrs.get('readonly'), 'readonly')


class UserViewsTest(TestCase):
    """Тесты для представлений пользователя"""
    
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # Создаем временную директорию для медиа файлов
        self.temp_media_dir = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self.temp_media_dir
    
    def tearDown(self):
        # Удаляем временную директорию
        if os.path.exists(self.temp_media_dir):
            shutil.rmtree(self.temp_media_dir)
    
    def test_login_view_get(self):
        """Тест GET запроса к странице логина"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Home - Авторизация')
    
    def test_login_view_post_valid(self):
        """Тест POST запроса с валидными данными для логина"""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # После успешного логина должен быть редирект
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('catalog:product_list'))
        
        # Проверяем что пользователь авторизован
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин если не авторизован
    
    def test_login_view_post_invalid(self):
        """Тест POST запроса с невалидными данными для логина"""
        response = self.client.post(reverse('users:login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        
        # Должен остаться на той же странице с формой
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertTrue(response.context['form'].errors)
    
    def test_registration_view_get(self):
        """Тест GET запроса к странице регистрации"""
        response = self.client.get(reverse('users:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertIn('form', response.context)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Home - Регистрация')
    
    def test_registration_view_post_valid(self):
        """Тест POST запроса с валидными данными для регистрации"""
        response = self.client.post(reverse('users:registration'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        
        # После успешной регистрации должен быть редирект
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('catalog:product_list'))
        
        # Проверяем что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_registration_view_post_invalid(self):
        """Тест POST запроса с невалидными данными для регистрации"""
        response = self.client.post(reverse('users:registration'), {
            'username': '',  # Пустое имя пользователя
            'email': 'invalid-email',
            'password1': 'pass',
            'password2': 'different'  # Пароли не совпадают
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertTrue(response.context['form'].errors)
    
    def test_profile_view_unauthorized(self):
        """Тест доступа к профилю без авторизации"""
        response = self.client.get(reverse('users:profile'))
        
        # Должен быть редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('users:login')))
    
    def test_profile_view_authorized(self):
        """Тест доступа к профилю с авторизацией"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('form', response.context)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Home - Кабинет')
        self.assertEqual(response.context['user'], self.user)
    
    def test_profile_view_post_valid(self):
        """Тест POST запроса с валидными данными для обновления профиля"""
        self.client.login(username='testuser', password='testpass123')
        
        # Создаем тестовое изображение
        image_content = b'test image content'
        image = SimpleUploadedFile(
            'test_image.jpg',
            image_content,
            content_type='image/jpeg'
        )
        
        response = self.client.post(reverse('users:profile'), {
            'username': 'testuser',  # Не меняется, поле readonly
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'Name',
            'image': image
        })
        
        # После успешного обновления должен быть редирект на ту же страницу
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile'))
        
        # Обновляем данные пользователя из базы
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertTrue(self.user.image.name.endswith('test_image.jpg'))
    
    def test_logout_view(self):
        """Тест выхода из системы"""
        # Сначала логинимся
        self.client.login(username='testuser', password='testpass123')
        
        # Проверяем что пользователь авторизован
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        
        # Выходим
        response = self.client.get(reverse('users:logout'))
        
        # Должен быть редирект на каталог
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('catalog:product_list'))
        
        # Проверяем что пользователь разлогинен
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_profile_view_cart_context(self):
        """Тест что корзина передается в контекст профиля"""
        self.client.login(username='testuser', password='testpass123')
        
        # Импортируем здесь, чтобы избежать циклических импортов
        from cart.models import Cart, CartItem
        
        response = self.client.get(reverse('users:profile'))
        
        self.assertIn('cart_items', response.context)
        self.assertIn('cart_total', response.context)
        
        # Проверяем типы данных
        self.assertIsInstance(response.context['cart_items'], list)
        self.assertIsInstance(response.context['cart_total'], (int, float))


class UserIntegrationTest(TestCase):
    """Интеграционные тесты для пользователя"""
    
    def test_full_user_flow(self):
        """Тест полного цикла пользователя: регистрация → логин → профиль → выход"""
        client = Client()
        
        # 1. Регистрация
        response = client.post(reverse('users:registration'), {
            'username': 'integrationuser',
            'email': 'integration@example.com',
            'password1': 'integrationpass123',
            'password2': 'integrationpass123',
        }, follow=True)  # follow=True чтобы следовать за редиректом
        
        # Проверяем что регистрация прошла успешно
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('catalog:product_list'))
        
        # Проверяем что пользователь создан
        self.assertTrue(User.objects.filter(username='integrationuser').exists())
        user = User.objects.get(username='integrationuser')
        
        # Проверяем что пользователь автоматически авторизован после регистрации
        response = client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Выход
        client.get(reverse('users:logout'))
        
        # Проверяем что пользователь разлогинен
        response = client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        
        # 3. Логин снова
        response = client.post(reverse('users:login'), {
            'username': 'integrationuser',
            'password': 'integrationpass123'
        }, follow=True)
        
        self.assertRedirects(response, reverse('catalog:product_list'))
        
        # Проверяем что снова авторизован
        response = client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_registration_with_existing_username(self):
        """Тест регистрации с уже существующим именем пользователя"""
        # Создаем пользователя
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )
        
        client = Client()
        
        # Пытаемся зарегистрироваться с тем же именем
        response = client.post(reverse('users:registration'), {
            'username': 'existinguser',  # Уже существует
            'email': 'newemail@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        
        # Должна остаться на странице с ошибкой
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        
        # Должна быть ошибка в форме
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)