"""
URL configuration for cosmetics_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),   
    path('register/', views.register_with_form, name='register'), 
    path('register/form/', views.register_with_form, name='register_form'),    # 
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('dashboard/<int:order_id>/', views.order_detail, name='order_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.view_cart, name='cart'),  
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('products/', views.product_list, name='products'), 
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

