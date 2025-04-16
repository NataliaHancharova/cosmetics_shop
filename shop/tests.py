from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Product, Cart, CartProduct, Order, OrderProduct
from .forms import CustomUserCreationForm
from decimal import Decimal

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone='+1234567890')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone, '+1234567890')

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
        self.cart_product = CartProduct.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, 'testuser')

    def test_cart_product_creation(self):
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

class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone': '+1234567890'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'differentpassword',
            'phone': '+1234567890'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

# class RegistrationTest(TestCase):
#     def test_registration_creates_profile(self):
#         form_data = {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password1': 'strongpassword123',
#             'password2': 'strongpassword123',
#             'phone': '+1234567890'
#         }
#         form = CustomUserCreationForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user = form.save()
#         profile = Profile.objects.get(user=user)
#         print(f"Профиль создан с телефоном: {profile.phone}")
#         self.assertEqual(profile.phone, '+1234567890')