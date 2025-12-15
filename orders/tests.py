import pytest
from django.test import TestCase
from .models import Order, OrderItem
from catalog.models import Product, Category, Brand
from users.models import User


class OrderBasicTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            email='user1@mail.ru',
            password='12345'
        )

        self.category = Category.objects.create(
            name='Телефоны',
            slug='phones'
        )

        self.brand = Brand.objects.create(
            name='Samsung',
            slug='samsung'
        )

        self.product = Product.objects.create(
            product_name='Galaxy S23',
            price=80000,
            category=self.category,
            brand=self.brand
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total=80000,
            full_name='Иван Петров',
            email='ivan@mail.ru',
            phone='89991234567',
            address='Москва'
        )

        assert order is not None
        assert order.user == self.user
        assert order.total == 80000

        assert order.number is not None
        assert 'ORDER-' in order.number

        assert 'Заказ #' in str(order)

    def test_order_with_items(self):
        order = Order.objects.create(
            user=self.user,
            total=0,
            full_name='Петр Сидоров',
            email='petr@yandex.ru',
            phone='+79215556677',
            address='Санкт-Петербург'
        )

        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            price=80000,
            quantity=2
        )

        assert order_item.sum == 160000
        assert order_item.product == self.product
        assert f'{self.product.product_name} x 2' == str(order_item)

    def test_order_statuses(self):
        order = Order.objects.create(
            user=self.user,
            total=50000,
            full_name='Анна Иванова',
            email='anna@gmail.com',
            phone='89031112233',
            address='Казань'
        )

        assert order.status == 'new'
        assert order.get_status_display() == 'Новый'

        order.status = 'confirmed'
        order.save()
        assert order.status == 'confirmed'

    def test_order_payment(self):
        order = Order.objects.create(
            user=self.user,
            total=60000,
            full_name='Сергей Кузнецов',
            email='sergey@mail.ru',
            phone='89167778899',
            address='Екатеринбург',
            payment='online'
        )

        assert order.payment == 'online'
        assert order.get_payment_display() == 'Онлайн'
        assert not order.is_paid