import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Cart, CartItem
from catalog.models import Product, Category, Brand
from users.models import User


class CartBasicTests(TestCase):
    """Базовые тесты для корзины"""

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Создаем категорию
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Создаем бренд
        self.brand = Brand.objects.create(
            name='Test Brand',
            slug='test-brand',
            description='Test brand description'
        )

        # Создаем продукт
        self.product = Product.objects.create(
            product_name='Test Product',
            description='Test product description',
            slug='test-product',
            price=100.00,
            category=self.category,
            brand=self.brand,
            stock=10
        )

    def test_cart_creation(self):
        """Тест 1: Создание корзины"""
        cart = Cart.objects.create(user=self.user)

        # Проверяем, что корзина создана
        self.assertIsNotNone(cart)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.total(), 0)
        self.assertEqual(cart.item_count(), 0)

    def test_add_item_to_cart(self):
        """Тест 2: Добавление товара в корзину"""
        cart = Cart.objects.create(user=self.user)

        # Добавляем товар в корзину
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=3
        )

        # Проверяем, что товар добавлен
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.total(), 300.00)  # 3 * 100
        self.assertEqual(cart.total(), 300.00)
        self.assertEqual(cart.item_count(), 1)

    def test_cart_string_representation(self):
        """Тест 3: Проверка строкового представления"""
        # Корзина с пользователем
        cart_user = Cart.objects.create(user=self.user)
        self.assertIn(self.user.username, str(cart_user))

        # Корзина с сессией
        cart_session = Cart.objects.create(session="abc123")
        self.assertIn("abc123", str(cart_session))

    def test_cart_with_multiple_items(self):
        """Тест 4: Корзина с несколькими товарами"""
        cart = Cart.objects.create(user=self.user)

        # Создаем второй товар
        product2 = Product.objects.create(
            product_name='Test Product 2',
            description='Another product',
            slug='test-product-2',
            price=50.00,
            category=self.category,
            brand=self.brand,
            stock=5
        )

        # Добавляем два товара
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)  # 2 * 100 = 200
        CartItem.objects.create(cart=cart, product=product2, quantity=3)  # 3 * 50 = 150

        # Проверяем общую сумму
        self.assertEqual(cart.total(), 350.00)  # 200 + 150
        self.assertEqual(cart.item_count(), 2)

    def test_empty_cart(self):
        """Тест 5: Пустая корзина"""
        cart = Cart.objects.create(user=self.user)

        self.assertEqual(cart.total(), 0)
        self.assertEqual(cart.item_count(), 0)


# Pytest тесты для запуска через pytest
@pytest.mark.django_db
def test_pytest_cart_workflow():
    """Pytest тест: полный рабочий процесс корзины"""
    # Создаем пользователя
    user = User.objects.create_user(
        username='pytestuser',
        email='pytest@example.com',
        password='testpass'
    )

    # Создаем категорию и бренд
    category = Category.objects.create(name='Category', slug='category')
    brand = Brand.objects.create(name='Brand', slug='brand', description='Brand')

    # Создаем товар
    product = Product.objects.create(
        product_name='Product',
        description='Description',
        slug='product',
        price=75.00,
        category=category,
        brand=brand,
        stock=10
    )

    # Создаем корзину
    cart = Cart.objects.create(user=user)
    assert cart.total() == 0

    # Добавляем товар
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2
    )

    # Проверяем
    assert cart_item.total() == 150.00  # 2 * 75
    assert cart.total() == 150.00
    assert cart.item_count() == 1
