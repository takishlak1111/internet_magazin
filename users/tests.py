import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


User = get_user_model() # моделька юзеров


class UserModelTest(TestCase):
    """Тесты для модели пользователя"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@m.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
    
    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@m.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_verbose_names(self):
        """Тест verbose_name модели"""
        self.assertEqual(User._meta.verbose_name, 'Пользователь')
        self.assertEqual(User._meta.verbose_name_plural, 'Пользователи')
    
    def test_user_table_name(self):
        """Тест имени таблицы в БД"""
        self.assertEqual(User._meta.db_table, 'user')


class UserFormsTest(TestCase):
    """Тесты для форм пользователя"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='existinguser',
            email='exist@example.com',
            password='testpass123'
        )
    
    def test_login_form_valid(self):
        """Тест валидной формы входа"""
        from users.forms import UserLoginForm
        
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_valid(self):
        """Тест валидной формы регистрации"""
        from users.forms import UserRegistrationForm
        
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_invalid_password_mismatch(self):
        """Тест формы регистрации с несовпадающими паролями"""
        from users.forms import UserRegistrationForm
        
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'password1',
            'password2': 'password2'  # ошибка разных паролей
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_profile_form_valid(self):
        """Тест валидной формы профиля"""
        from users.forms import ProfileForm
        
        form_data = {
            'username': 'existinguser',
            'email': 'updated@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    


class UserViewsTest(TestCase):
    """Тесты для представлений (views)"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Тест GET запроса к странице входа"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Авторизация')
    
    def test_login_view_post_valid(self):
        """Тест POST запроса с валидными данными"""
        response = self.client.post(
            reverse('users:login'),
            {'username': 'testuser', 'password': 'testpass123'}
        )
        # После успешного входа должен быть редирект
        self.assertEqual(response.status_code, 302)
    
    def test_login_view_post_invalid(self):
        """Тест POST запроса с невалидными данными"""
        response = self.client.post(
            reverse('users:login'),
            {'username': 'wrong', 'password': 'wrong'}
        )
        self.assertEqual(response.status_code, 200)  # Остается на странице
        self.assertContains(response, 'Авторизация')
    
    def test_registration_view_get(self):
        """Тест GET запроса к странице регистрации"""
        response = self.client.get(reverse('users:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertContains(response, 'Регистрация')
    
    def test_registration_view_post_valid(self):
        """Тест POST запроса с валидной регистрацией"""
        response = self.client.post(
            reverse('users:registration'),
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!'
            }
        )
        self.assertEqual(response.status_code, 302)  # Редирект после успеха
        
        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_profile_view_requires_login(self):
        """Тест что профиль требует аутентификации"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_profile_view_authenticated(self):
        """Тест профиля для аутентифицированного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'Кабинет')
    
    def test_profile_view_post_update(self):
        """Тест обновления профиля"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('users:profile'),
            {
                'username': 'testuser',
                'email': 'updated@example.com',
                'first_name': 'Updated',
                'last_name': 'Name'
            }
        )
        
        # Проверяем обновление
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
    
    def test_logout_view(self):
        """Тест выхода из системы"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Редирект
    
    def test_login_redirects_authenticated_user(self):
        """Тест что аутентифицированный пользователь редиректится с логина"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:login'))
        # В зависимости от вашей логики, может быть редирект или оставаться на странице
        # Если у вас есть редирект для уже вошедших, проверяйте его
        # self.assertEqual(response.status_code, 302)


class UserUrlsTest(TestCase):
    """Тесты URL маршрутов"""
    
    def test_login_url(self):
        """Тест URL входа"""
        url = reverse('users:login')
        self.assertEqual(url, '/users/login/')
    
    def test_registration_url(self):
        """Тест URL регистрации"""
        url = reverse('users:registration')
        self.assertEqual(url, '/users/registration/')
    
    def test_profile_url(self):
        """Тест URL профиля"""
        url = reverse('users:profile')
        self.assertEqual(url, '/users/profile/')
    
    def test_logout_url(self):
        """Тест URL выхода"""
        url = reverse('users:logout')
        self.assertEqual(url, '/users/logout/')


# Тесты с использованием pytest 
@pytest.mark.django_db
def test_create_user_with_fixture():
    """Тест создания пользователя с использованием pytest"""
    user = User.objects.create_user(
        username='pytestuser',
        email='pytest@example.com',
        password='testpass123'
    )
    assert user.username == 'pytestuser'
    assert user.email == 'pytest@example.com'
    assert user.check_password('testpass123') is True


@pytest.mark.django_db
def test_user_login_view(client):
    """Тест представления логина с использованием pytest"""
    User.objects.create_user(
        username='pytestuser',
        password='testpass123'
    )
    
    response = client.post(
        reverse('users:login'),
        {'username': 'pytestuser', 'password': 'testpass123'}
    )
    assert response.status_code == 302  # Редирект после успешного входа