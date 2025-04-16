from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Product, Cart, CartProduct, Order, OrderProduct
from decimal import Decimal

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Добавляем значение для поля address
        self.profile = Profile.objects.create(user=self.user, phone='+1234567890', address='Test Address')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone, '+1234567890')
        self.assertEqual(self.profile.address, 'Test Address')  # Проверяем поле address

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            image='product_images/test.jpg'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            image='product_images/test.jpg'
        )
        self.cart = Cart.objects.create(user=self.user)
        # Убедимся, что продукт добавляется в корзину только в тесте cart_product_creation
        self.cart_product = CartProduct.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_creation(self):
        # Проверяем, что корзина создаётся без продуктов
        self.assertEqual(CartProduct.objects.filter(cart=self.cart).count(), 0)

    def test_cart_product_creation(self):
        # Проверяем, что продукт добавляется в корзину
        self.assertEqual(self.cart_product.product.name, 'Test Product')
        self.assertEqual(self.cart_product.quantity, 2)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            image='product_images/test.jpg'
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=Decimal('199.98'),
            quantity=2,
            status='Pending'
        )
        self.order_product = OrderProduct.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.total_price, Decimal('199.98'))
        self.assertEqual(self.order.status, 'Pending')

    def test_order_product_creation(self):
        self.assertEqual(self.order_product.product.name, 'Test Product')
        self.assertEqual(self.order_product.quantity, 2)
