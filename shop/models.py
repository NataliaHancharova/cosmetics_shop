from django.db import models 
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(attrs={'placeholder': '+999999999'}),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            print(f"Сохранение профиля с телефоном: {self.cleaned_data['phone']}")  # Отладочный вывод
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
            )
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя пользователя уже занято.")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email    
class Product(models.Model):   #информация о продукте
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name

class Cart(models.Model):  #корзина
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')

class CartProduct(models.Model):  #продукты в корзине
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):  #заказ
    id = models.AutoField(primary_key=True)  #уникальный идентификатор заказа
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    ]   
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in order {self.order.id}"
    
class Profile(models.Model):   #профиль пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате: '+999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username





