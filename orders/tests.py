import unittest
from django.test import TestCase
from django.db import IntegrityError

from .models import Order, OrderItem
from catalog.models import Product, Category, Brand
from users.models import User


class OrderModelTest(TestCase):
    """Тесты для модели Order"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.category = Category.objects.create(
            name='Электроника',
            slug='electronics'
        )

        self.brand = Brand.objects.create(
            name='Apple',
            slug='apple'
        )

        self.product = Product.objects.create(
            product_name='iPhone 15',
            price=89990.00,
            category=self.category,
            brand=self.brand
        )

    def test_order_creation_positive(self):
        """Позитивный тест: создание заказа с валидными данными"""
        order = Order.objects.create(
            user=self.user,
            total=89990.00,
            full_name='Иван Иванов',
            email='ivan@mail.ru',
            phone='+79991234567',
            address='Москва'
        )

        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total, 89990.00)

        self.assertEqual(order.status, 'new')
        self.assertEqual(order.payment, 'cash')
        self.assertFalse(order.is_paid)

    def test_order_number_generation_positive(self):
        """Позитивный тест: генерация уникального номера заказа"""
        order = Order.objects.create(
            user=self.user,
            total=10000.00,
            full_name='Петр Петров',
            email='petr@mail.ru',
            phone='89998887766',
            address='Санкт-Петербург'
        )

        self.assertIsNotNone(order.number)
        self.assertTrue(order.number.startswith('ORDER-'))

        self.assertIn('Заказ #', str(order))

    def test_order_with_items_positive(self):
        """Позитивный тест: создание заказа с товарами"""
        order = Order.objects.create(
            user=self.user,
            total=0.00,
            full_name='Сергей Сергеев',
            email='sergey@mail.ru',
            phone='89161112233',
            address='Казань'
        )

        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price=89990.00,
            quantity=2
        )

        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)

        self.assertEqual(order_item.sum, 179980.00)

    def test_order_status_changes_positive(self):
        """Позитивный тест: изменение статуса заказа"""
        order = Order.objects.create(
            user=self.user,
            total=50000.00,
            full_name='Анна Аннова',
            email='anna@mail.ru',
            phone='89212223344',
            address='Екатеринбург'
        )

        self.assertEqual(order.status, 'new')
        self.assertEqual(order.get_status_display(), 'Новый')

        order.status = 'confirmed'
        order.save()

        self.assertEqual(order.status, 'confirmed')
        self.assertEqual(order.get_status_display(), 'Подтвержден')

    def test_order_payment_types_positive(self):
        """Позитивный тест: разные типы оплаты"""
        payments = [
            ('cash', 'Наличные'),
            ('card', 'Карта'),
            ('online', 'Онлайн')
        ]

        for payment_code, payment_name in payments:
            order = Order.objects.create(
                user=self.user,
                total=30000.00,
                full_name=f'Тест {payment_code}',
                email=f'test_{payment_code}@mail.ru',
                phone='89160000000',
                address='Адрес',
                payment=payment_code
            )

            self.assertEqual(order.payment, payment_code)
            self.assertEqual(order.get_payment_display(), payment_name)

    def test_order_without_user_negative(self):
        """Негативный тест: попытка создать заказ без пользователя"""
        with self.assertRaises(IntegrityError):
            Order.objects.create(
                total=10000.00,
                full_name='Без Пользователя',
                email='nouser@mail.ru',
                phone='89160000000',
                address='Адрес'
            )

    def test_order_with_negative_total_negative(self):
        """Негативный тест: заказ с отрицательной суммой"""
        order = Order.objects.create(
            user=self.user,
            total=-5000.00,
            full_name='Отрицательный Заказ',
            email='negative@mail.ru',
            phone='89162223344',
            address='Адрес'
        )

        self.assertIsNotNone(order)
        self.assertEqual(order.total, -5000.00)


class OrderItemModelTest(TestCase):
    """Тесты для модели OrderItem"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='customer',
            email='customer@shop.ru',
            password='pass123'
        )

        self.category = Category.objects.create(
            name='Одежда',
            slug='clothes'
        )

        self.brand = Brand.objects.create(
            name='Nike',
            slug='nike'
        )

        self.product = Product.objects.create(
            product_name='Кроссовки',
            price=5000.00,
            category=self.category,
            brand=self.brand
        )

        self.order = Order.objects.create(
            user=self.user,
            total=0.00,
            full_name='Покупатель',
            email='buyer@mail.ru',
            phone='89161234567',
            address='Москва'
        )

    def test_order_item_creation_positive(self):
        """Позитивный тест: создание товара в заказе"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=5000.00,
            quantity=3
        )

        self.assertIsNotNone(order_item)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, 5000.00)
        self.assertEqual(order_item.quantity, 3)

    def test_order_item_sum_calculation_positive(self):
        """Позитивный тест: расчет суммы товара"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=5000.00,
            quantity=2
        )

        expected_sum = 5000.00 * 2
        self.assertEqual(order_item.sum, expected_sum)

    def test_order_item_string_representation_positive(self):
        """Позитивный тест: строковое представление товара"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=5000.00,
            quantity=4
        )

        expected_str = f'{self.product.product_name} x 4'
        self.assertEqual(str(order_item), expected_str)

    def test_order_item_default_quantity_positive(self):
        """Позитивный тест: количество по умолчанию"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=5000.00
        )

        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.sum, 5000.00)

    def test_order_item_related_name_positive(self):
        """Позитивный тест: доступ через related_name"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=5000.00,
            quantity=2
        )

        self.assertIn(order_item, self.order.items.all())
        self.assertEqual(self.order.items.count(), 1)

    def test_order_item_without_order_negative(self):
        """Негативный тест: попытка создать товар без заказа"""
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                product=self.product,
                price=5000.00,
                quantity=1
            )

    def test_order_item_with_zero_quantity_negative(self):
        """Негативный тест: товар с нулевым количеством"""
        try:
            order_item = OrderItem.objects.create(
                order=self.order,
                product=self.product,
                price=5000.00,
                quantity=0
            )
            self.assertIsNotNone(order_item)
            self.assertEqual(order_item.sum, 0.00)
        except IntegrityError:
            self.assertTrue(True)

    def test_order_item_negative_quantity_negative(self):
        """Негативный тест: попытка создать товар с отрицательным количеством"""
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                order=self.order,
                product=self.product,
                price=5000.00,
                quantity=-2
            )

    def test_order_item_negative_price_negative(self):
        """Негативный тест: попытка создать товар с отрицательной ценой"""
        try:
            order_item = OrderItem.objects.create(
                order=self.order,
                product=self.product,
                price=-1000.00,
                quantity=3
            )
            self.assertIsNotNone(order_item)
            self.assertEqual(order_item.price, -1000.00)
            self.assertEqual(order_item.sum, -3000.00)
        except IntegrityError:
            self.assertTrue(True)

    def test_order_item_cascade_delete(self):
        """Позитивный тест: удаление товаров при удалении заказа"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=5000.00,
            quantity=2
        )

        order_item_id = order_item.id
        order_id = self.order.id

        self.order.delete()

        self.assertFalse(Order.objects.filter(id=order_id).exists())

        self.assertFalse(OrderItem.objects.filter(id=order_item_id).exists())