# tests/test_reviews.py
import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from catalog.models import Product, Category  # Добавляем импорт Category
from reviews.models import Review
from reviews.forms import ReviewForm

User = get_user_model()


@pytest.mark.django_db
class TestReviewModel:
    """Ключевые тесты для модели Review"""

    def setup_method(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Создаем категорию (используем name вместо category_name)
        self.category = Category.objects.create(
            name='Test Category',  # Изменено с category_name на name
            slug='test-category'
        )
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            price=1000.00,
            category=self.category  # Добавляем обязательную категорию
        )

    def test_create_and_str_method(self):
        """Тест создания отзыва и строкового представления"""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            text='Отличный товар!'
        )

        # Проверяем создание
        assert review.product == self.product
        assert review.user == self.user
        assert review.rating == 5
        assert review.text == 'Отличный товар!'

        # Проверяем строковое представление
        expected_str = f'{self.user} - {self.product} (5⭐)'
        assert str(review) == expected_str

    def test_rating_validation(self):
        """Тест валидации рейтинга (граничные значения)"""
        # Тест минимального значения
        review_min = Review(
            product=self.product,
            user=self.user,
            rating=0
        )
        with pytest.raises(ValidationError):
            review_min.full_clean()

        # Тест максимального значения
        review_max = Review(
            product=self.product,
            user=self.user,
            rating=6
        )
        with pytest.raises(ValidationError):
            review_max.full_clean()

        # Тест валидного значения
        review_valid = Review(
            product=self.product,
            user=self.user,
            rating=3
        )
        try:
            review_valid.full_clean()
        except ValidationError:
            pytest.fail("Рейтинг 3 должен быть валидным")

    def test_default_values_and_blank_text(self):
        """Тест значений по умолчанию и необязательных полей"""
        review = Review.objects.create(
            product=self.product,
            user=self.user
        )

        # Проверяем значение по умолчанию
        assert review.rating == 5

        # Проверяем, что текст может быть пустым
        review.text = ''
        review.full_clean()  # Не должно вызывать ошибку


@pytest.mark.django_db
class TestReviewForm:
    """Ключевые тесты для формы ReviewForm"""

    def test_valid_and_invalid_data(self):
        """Тест валидных и невалидных данных"""
        # Валидные данные
        valid_data = {'rating': 5, 'text': 'Отличный товар!'}
        form = ReviewForm(data=valid_data)
        assert form.is_valid()
        assert form.cleaned_data['rating'] == 5

        # Невалидные данные (рейтинг вне диапазона)
        invalid_data = {'rating': 6, 'text': 'Отлично'}
        form = ReviewForm(data=invalid_data)
        assert not form.is_valid()
        assert 'rating' in form.errors

        # Отсутствует обязательное поле
        missing_data = {'text': 'Без рейтинга'}
        form = ReviewForm(data=missing_data)
        assert not form.is_valid()
        assert 'rating' in form.errors

    def test_form_fields_and_widgets(self):
        """Тест полей формы и виджетов"""
        form = ReviewForm()

        # Проверяем поля
        assert list(form.fields.keys()) == ['rating', 'text']

        # Проверяем виджет для rating (Select)
        assert form.fields['rating'].widget.__class__.__name__ == 'Select'
        assert len(list(form.fields['rating'].widget.choices)) == 5

        # Проверяем виджет для text (Textarea с атрибутами)
        textarea = form.fields['text'].widget
        assert textarea.__class__.__name__ == 'Textarea'
        assert textarea.attrs.get('rows') == 3
        assert textarea.attrs.get('placeholder') == 'Ваш отзыв...'


@pytest.mark.django_db
class TestAddReviewView:
    """Основные тесты для представления add_review"""

    def setup_method(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Создаем категорию
        self.category = Category.objects.create(
            name='Test Category',  # Изменено с category_name на name
            slug='test-category'
        )
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            price=1000.00,
            category=self.category  # Добавляем обязательную категорию
        )
        self.url = reverse('reviews:add_review', args=[self.product.id])

    def test_successful_review_creation(self, client):
        """Успешное создание отзыва"""
        client.force_login(self.user)
        data = {'rating': 5, 'text': 'Отличный товар!'}

        response = client.post(self.url, data)

        # Проверяем редирект
        assert response.status_code == 302

        # Проверяем создание отзыва
        assert Review.objects.filter(
            product=self.product,
            user=self.user
        ).exists()

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        assert 'Отзыв добавлен!' in str(messages[0])

    def test_duplicate_review_prevention(self, client):
        """Защита от создания дубликата отзыва"""
        client.force_login(self.user)

        # Создаем первый отзыв
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5
        )

        # Пытаемся создать второй
        data = {'rating': 3, 'text': 'Второй отзыв'}
        response = client.post(self.url, data)

        # Проверяем, что второй не создан
        reviews = Review.objects.filter(product=self.product, user=self.user)
        assert reviews.count() == 1

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        assert 'Вы уже оставили отзыв' in str(messages[0])

    def test_authentication_required(self, client):
        """Требуется авторизация"""
        response = client.get(self.url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_invalid_form_handling(self, client):
        """Обработка невалидной формы"""
        client.force_login(self.user)
        data = {'rating': 6}  # Невалидный рейтинг

        response = client.post(self.url, data)

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        assert 'Пожалуйста, выберите оценку' in str(messages[0])


@pytest.mark.django_db
class TestDeleteReviewView:
    """Основные тесты для представления delete_review"""

    def setup_method(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )

        # Создаем категорию
        self.category = Category.objects.create(
            name='Test Category',  # Изменено с category_name на name
            slug='test-category'
        )

        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            price=1000.00,
            category=self.category  # Добавляем обязательную категорию
        )

        self.review = Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5
        )

    def test_successful_deletion(self, client):
        """Успешное удаление своего отзыва"""
        client.force_login(self.user1)
        url = reverse('reviews:delete_review', args=[self.review.id])

        response = client.post(url)

        # Проверяем редирект
        assert response.status_code == 302

        # Проверяем удаление
        assert not Review.objects.filter(id=self.review.id).exists()

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        assert 'Отзыв удален!' in str(messages[0])

    def test_cannot_delete_other_users_review(self, client):
        """Нельзя удалить чужой отзыв"""
        client.force_login(self.user2)  # Другой пользователь
        url = reverse('reviews:delete_review', args=[self.review.id])

        response = client.post(url)

        # Должен вернуть 404
        assert response.status_code == 404

        # Отзыв должен остаться
        assert Review.objects.filter(id=self.review.id).exists()

    def test_authentication_required_for_deletion(self, client):
        """Для удаления требуется авторизация"""
        url = reverse('reviews:delete_review', args=[self.review.id])
        response = client.post(url)

        assert response.status_code == 302
        assert '/login/' in response.url


@pytest.mark.django_db
def test_full_review_workflow(client):
    """Полный цикл работы с отзывами"""
    # Создаем тестовые данные
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

    # Создаем категорию
    category = Category.objects.create(
        name='Test Category',  # Изменено с category_name на name
        slug='test-category'
    )

    product = Product.objects.create(
        product_name='Test Product',
        slug='test-product',
        price=1000.00,
        category=category  # Добавляем обязательную категорию
    )

    client.force_login(user)

    # 1. Добавляем отзыв
    add_url = reverse('reviews:add_review', args=[product.id])
    client.post(add_url, {'rating': 4, 'text': 'Хороший товар'})

    # Проверяем, что отзыв создан
    review = Review.objects.filter(product=product, user=user).first()
    assert review is not None
    assert review.rating == 4

    # 2. Пытаемся добавить второй отзыв (не должен создаться)
    client.post(add_url, {'rating': 5, 'text': 'Второй отзыв'})
    reviews = Review.objects.filter(product=product, user=user)
    assert reviews.count() == 1  # Только один отзыв

    # 3. Удаляем отзыв
    delete_url = reverse('reviews:delete_review', args=[review.id])
    client.post(delete_url)

    # Проверяем, что отзыв удален
    assert not Review.objects.filter(id=review.id).exists()
