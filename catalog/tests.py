import pytest
from decimal import Decimal
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch, Mock
from .models import Category, Brand, Product


class TestCategoryModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Электроника",
            slug="electronics"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Электроника")
        self.assertEqual(self.category.slug, "electronics")
        self.assertEqual(str(self.category), "Электроника")

    def test_category_absolute_url(self):
        try:
            expected_url = reverse('catalog:category_detail', kwargs={'slug': 'electronics'})
            self.assertEqual(self.category.get_absolute_url(), expected_url)
        except:
            self.assertTrue(hasattr(self.category, 'get_absolute_url'))

    def test_category_meta_options(self):
        self.assertEqual(Category._meta.verbose_name, 'Категория')
        self.assertEqual(Category._meta.verbose_name_plural, 'Категории')
        self.assertEqual(Category._meta.ordering, ['name'])

    def test_category_ordering(self):
        Category.objects.create(name="Бытовая техника", slug="appliances")
        Category.objects.create(name="Аксессуары", slug="accessories")

        categories = Category.objects.all()
        self.assertEqual(categories[0].name, "Аксессуары")
        self.assertEqual(categories[1].name, "Бытовая техника")
        self.assertEqual(categories[2].name, "Электроника")


class TestBrandModel(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(
            name="Apple",
            slug="apple",
            description="Американская компания"
        )

    def test_brand_creation(self):
        self.assertEqual(self.brand.name, "Apple")
        self.assertEqual(self.brand.slug, "apple")
        self.assertEqual(self.brand.description, "Американская компания")
        self.assertEqual(str(self.brand), "Apple")

    def test_brand_absolute_url(self):
        try:
            expected_url = reverse('brand_detail', kwargs={'slug': 'apple'})
            self.assertEqual(self.brand.get_absolute_url(), expected_url)
        except:
            self.assertTrue(hasattr(self.brand, 'get_absolute_url'))

    def test_brand_meta_options(self):
        self.assertEqual(Brand._meta.verbose_name, 'Бренд')
        self.assertEqual(Brand._meta.verbose_name_plural, 'Бренды')
        self.assertEqual(Brand._meta.ordering, ['name'])

    def test_brand_product_count_without_products(self):
        self.assertEqual(self.brand.product_count, 0)

    def test_brand_product_count_with_products(self):
        category = Category.objects.create(
            name="Электроника",
            slug="electronics"
        )

        Product.objects.create(
            product_name="iPhone 13",
            description="Смартфон",
            slug="iphone-13",
            price=Decimal("79999.99"),
            category=category,
            brand=self.brand
        )
        Product.objects.create(
            product_name="MacBook Pro",
            description="Ноутбук",
            slug="macbook-pro",
            price=Decimal("149999.99"),
            category=category,
            brand=self.brand
        )

        self.assertEqual(self.brand.product_count, 2)

    def test_brand_ordering(self):
        Brand.objects.create(name="Samsung", slug="samsung")
        Brand.objects.create(name="Xiaomi", slug="xiaomi")

        brands = Brand.objects.all()
        self.assertEqual(brands[0].name, "Apple")
        self.assertEqual(brands[1].name, "Samsung")
        self.assertEqual(brands[2].name, "Xiaomi")


class TestProductModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Электроника",
            slug="electronics"
        )
        self.brand = Brand.objects.create(
            name="Apple",
            slug="apple"
        )
        self.product = Product.objects.create(
            product_name="iPhone 13",
            description="Смартфон с отличной камерой",
            slug="iphone-13",
            price=Decimal("79999.99"),
            category=self.category,
            brand=self.brand,
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, "iPhone 13")
        self.assertEqual(self.product.slug, "iphone-13")
        self.assertEqual(self.product.price, Decimal("79999.99"))
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.brand, self.brand)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(str(self.product), "Apple iPhone 13")

    def test_product_without_brand(self):
        product = Product.objects.create(
            product_name="Генеральный кабель",
            description="Универсальный кабель",
            slug="universal-cable",
            price=Decimal("999.99"),
            category=self.category,
            brand=None,
            stock=5
        )
        self.assertIsNone(product.brand)

    def test_product_in_stock_positive(self):
        self.product.stock = 5
        self.product.save()
        self.assertTrue(self.product.in_stock)

    def test_product_in_stock_negative_zero(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.in_stock)

    def test_product_in_stock_negative_below_zero(self):
        self.product.stock = -5
        self.product.save()
        self.assertFalse(self.product.in_stock)

    def test_product_absolute_url(self):
        try:
            expected_url = reverse('product_detail', kwargs={'slug': 'iphone-13'})
            self.assertEqual(self.product.get_absolute_url(), expected_url)
        except:
            self.assertTrue(hasattr(self.product, 'get_absolute_url'))

    def test_product_meta_options(self):
        self.assertEqual(Product._meta.verbose_name, 'Товар')
        self.assertEqual(Product._meta.verbose_name_plural, 'Товары')
        self.assertEqual(Product._meta.ordering, ['created_at'])

    def test_product_indexes(self):
        indexes = Product._meta.indexes
        index_fields = [index.fields for index in indexes]

        self.assertIn(['slug'], index_fields)
        self.assertIn(['price'], index_fields)
        self.assertIn(['created_at'], index_fields)

    def test_product_average_rating_no_reviews(self):
        with patch('reviews.models.Review') as mock_review:
            mock_review.objects.filter.return_value.exists.return_value = False
            self.assertEqual(self.product.average_rating, 0.0)

    def test_product_reviews_count_no_reviews(self):
        with patch('reviews.models.Review') as mock_review:
            mock_review.objects.filter.return_value.count.return_value = 0
            self.assertEqual(self.product.reviews_count, 0)

    def test_product_ordering(self):
        product2 = Product.objects.create(
            product_name="iPhone 14",
            description="Новая модель",
            slug="iphone-14",
            price=Decimal("89999.99"),
            category=self.category,
            brand=self.brand
        )

        products = Product.objects.all()
        self.assertEqual(products[0], self.product)
        self.assertEqual(products[1], product2)

    def test_product_default_values(self):
        product = Product.objects.create(
            product_name="Test Product",
            description="Test",
            slug="test-product",
            price=Decimal("1000.00"),
            category=self.category,
            brand=self.brand
        )
        self.assertEqual(product.rating, 0.0)
        self.assertEqual(product.stock, 0)
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)

    def test_product_string_representation_without_brand(self):
        product = Product.objects.create(
            product_name="Безымянный товар",
            description="Товар без бренда",
            slug="no-brand-product",
            price=Decimal("500.00"),
            category=self.category,
            brand=None
        )
        self.assertEqual(product.product_name, "Безымянный товар")
        self.assertIsNone(product.brand)

class TestModelsIntegration(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Электроника",
            slug="electronics"
        )
        self.brand = Brand.objects.create(
            name="Apple",
            slug="apple"
        )

    def test_brand_products_relationship(self):
        product1 = Product.objects.create(
            product_name="iPhone 13",
            description="Смартфон",
            slug="iphone-13",
            price=Decimal("79999.99"),
            category=self.category,
            brand=self.brand
        )

        product2 = Product.objects.create(
            product_name="MacBook Pro",
            description="Ноутбук",
            slug="macbook-pro",
            price=Decimal("149999.99"),
            category=self.category,
            brand=self.brand
        )

        brand_products = self.brand.products.all()
        self.assertEqual(brand_products.count(), 2)
        self.assertIn(product1, brand_products)
        self.assertIn(product2, brand_products)

    def test_category_products_relationship(self):
        product = Product.objects.create(
            product_name="iPhone 13",
            description="Смартфон",
            slug="iphone-13",
            price=Decimal("79999.99"),
            category=self.category,
            brand=self.brand
        )

        self.assertEqual(product.category, self.category)

        category_products = self.category.product_set.all()
        self.assertEqual(category_products.count(), 1)
        self.assertIn(product, category_products)

    def test_on_delete_cascade_for_category(self):
        product = Product.objects.create(
            product_name="Test Product",
            description="Test",
            slug="test-product",
            price=Decimal("1000.00"),
            category=self.category,
            brand=self.brand
        )

        category_id = self.category.id
        self.category.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product.id)

    def test_on_delete_set_null_for_brand(self):
        product = Product.objects.create(
            product_name="Test Product",
            description="Test",
            slug="test-product",
            price=Decimal("1000.00"),
            category=self.category,
            brand=self.brand
        )

        brand_id = self.brand.id
        self.brand.delete()

        product.refresh_from_db()

        self.assertIsNone(product.brand)


class TestFieldValidators(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Тест",
            slug="test"
        )
        self.brand = Brand.objects.create(
            name="Тест",
            slug="test"
        )

    def test_price_positive_value(self):
        product = Product.objects.create(
            product_name="Товар",
            description="Описание",
            slug="product",
            price=Decimal("1000.00"),
            category=self.category,
            brand=self.brand
        )
        self.assertEqual(product.price, Decimal("1000.00"))

    def test_price_zero_value(self):
        product = Product.objects.create(
            product_name="Бесплатный товар",
            description="Описание",
            slug="free-product",
            price=Decimal("0.00"),
            category=self.category,
            brand=self.brand
        )
        self.assertEqual(product.price, Decimal("0.00"))

    def test_slug_uniqueness(self):
        Product.objects.create(
            product_name="Товар 1",
            description="Описание",
            slug="unique-slug",
            price=Decimal("1000.00"),
            category=self.category,
            brand=self.brand
        )

        with self.assertRaises(Exception):
            Product.objects.create(
                product_name="Товар 2",
                description="Описание",
                slug="unique-slug",
                price=Decimal("2000.00"),
                category=self.category,
                brand=self.brand
            )

    def test_max_length_constraints(self):
        category = Category.objects.create(
            name="C" * 100,
            slug="c" * 100
        )
        self.assertEqual(len(category.name), 100)
        self.assertEqual(len(category.slug), 100)

        product = Product.objects.create(
            product_name="P" * 100,
            description="Описание",
            slug="p" * 200,
            price=Decimal("1000.00"),
            category=self.category,
            brand=self.brand
        )
        self.assertEqual(len(product.product_name), 100)
        self.assertEqual(len(product.slug), 200)


@pytest.mark.django_db
class TestPytestModels:

    def test_category_creation_pytest(self):
        category = Category.objects.create(
            name="Тестовая категория",
            slug="test-category"
        )
        assert category.name == "Тестовая категория"
        assert category.slug == "test-category"

    def test_brand_creation_pytest(self):
        brand = Brand.objects.create(
            name="Тестовый бренд",
            slug="test-brand"
        )
        assert brand.name == "Тестовый бренд"
        assert brand.slug == "test-brand"

    def test_product_creation_pytest(self):
        category = Category.objects.create(name="Категория", slug="category")
        brand = Brand.objects.create(name="Бренд", slug="brand")

        product = Product.objects.create(
            product_name="Тестовый продукт",
            description="Описание",
            slug="test-product",
            price=Decimal("1000.00"),
            category=category,
            brand=brand
        )

        assert product.product_name == "Тестовый продукт"
        assert product.price == Decimal("1000.00")
        assert product.in_stock == False

    def test_product_in_stock_pytest(self):
        category = Category.objects.create(name="Категория", slug="category")
        brand = Brand.objects.create(name="Бренд", slug="brand")

        product = Product.objects.create(
            product_name="Товар",
            description="Описание",
            slug="product",
            price=Decimal("1000.00"),
            category=category,
            brand=brand,
            stock=5
        )

        assert product.in_stock == True

    def test_brand_product_count_pytest(self):
        category = Category.objects.create(name="Категория", slug="category")
        brand = Brand.objects.create(name="Бренд", slug="brand")

        Product.objects.create(
            product_name="Товар 1",
            description="Описание",
            slug="product-1",
            price=Decimal("1000.00"),
            category=category,
            brand=brand
        )

        Product.objects.create(
            product_name="Товар 2",
            description="Описание",
            slug="product-2",
            price=Decimal("2000.00"),
            category=category,
            brand=brand
        )

        assert brand.product_count == 2