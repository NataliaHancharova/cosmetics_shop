from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .forms import UserCreationForm
from django.http import HttpResponse
from .models import Product, Cart, CartProduct
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages


def home(request):
    products = Product.objects.all()  # Получение всех продуктов
    return render(request, 'home.html', {'products': products})


def register_with_form(request): # Регистрация пользователя с использованием формы
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались! Теперь вы можете войти.')  # Сохранение пользователя в базе данных
            return redirect('login') 
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def create_user(username, email, password): # Создание пользователя
    try:                     
        if User.objects.filter(username=username).exists(): # Проверка на существование пользователя
            return f"Пользователь с именем {username} уже существует."
        if User.objects.filter(email=email).exists():
            return f"Пользователь с email {email} уже зарегистрирован."
        validate_password(password) 
        user = User.objects.create_user(username=username, email=email, password=password)# Создание пользователя
        return f"Пользователь {user.username} успешно создан."
    except ValidationError as e:
        return f"Ошибка валидации: {e}"
    except Exception as e:
        return f"Произошла ошибка: {e}"
 
def user_login(request): # Вход пользователя
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')  # Перенаправление на страницу профиля после успешного входа
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Неверный логин или пароль.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})   
    
@login_required #
def user_dashboard(request):  #
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'orders': orders})


@login_required # Получение информации о пользователе
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user': request.user, 'orders': orders})

@login_required   # Получение информации о пользователе
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def order_history(request):  # Получение истории заказов пользователя
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

def order_detail(request, order_id): # Получение конкретного заказа пользователя или 404, если заказ не найден
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def add_to_cart(request, product_id):  # Добавление продукта в корзину
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_product, _ = CartProduct.objects.get_or_create(cart=cart, product=product)
    cart_product.quantity += 1
    cart_product.save()
    return redirect('cart')

def remove_from_cart(request, product_id): # Удаление продукта из корзины
    cart = get_object_or_404(Cart, user=request.user)
    cart_product = get_object_or_404(CartProduct, cart=cart, product_id=product_id)
    cart_product.delete()
    return redirect('cart')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = CartProduct.objects.filter(cart=cart)
    cart_items = []
    total_price = 0

    for item in cart_products:
        item_total = item.quantity * item.product.price
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total
        })
        total_price += item_total

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_products = CartProduct.objects.filter(cart=cart)
        if not cart_products.exists():
            messages.error(request, 'Ваша корзина пуста.')
            return redirect('cart')

        total_price = sum(item.product.price * item.quantity for item in cart_products)

        if request.method == 'POST':
            order = Order.objects.create(user=request.user, total_price=total_price)
            for item in cart_products:
                order.products.add(item.product)
            order.save()
            cart_products.delete()
            cart.delete()
            return redirect('order_confirmation')

        return render(request, 'checkout.html', {'cart_products': cart_products, 'total_price': total_price})
    except Cart.DoesNotExist:
        messages.error(request, 'У вас нет активной корзины.')
        return redirect('cart')

def products(request):
    products = Product.objects.all()  # Получение всех продуктов
    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})