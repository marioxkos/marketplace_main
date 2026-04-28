# 🚀 SPRINT 1 — Setup + Modelado Base
## 🎯 Objetivo
Tener:
*Proyecto Django funcionando
*App marketplace
*Modelos con relaciones:
    - 1:N → Usuario → Producto
    - N:M → Producto ↔ Categoría
    - N:M → Carrito ↔ Producto (con CartItem)
*Admin operativo

## 1 Crear proyecto en django
```bash
django-admin startproject marketplace_main
cd marketplace_main
python manage.py startapp store
```

## 2 Configurar settings.py
📌 Agregar app
```python
INSTALLED_APPS = [
    ...
    'store',
]
```
📌 Usuario personalizado
```python
AUTH_USER_MODEL = 'marketplace.User'
```

## 3 MODELOS (CLAVE DEL PROYECTO)
Diseño de la Base De Datos Relacional en Diagrama Entidad-Relacion
![Diagrama Entidad-Relacion](https://github.com/jcromerohdz/marketplace_main_2026/blob/main/Diagrama_Entidad_Ralacion.png)
📁 marketplace/models.py
```python
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# 👤 Usuario
# =========================
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# =========================
# 🏷️ Categoría
# =========================
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =========================
# 📦 Producto
# =========================
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )  # 1:N

    categories = models.ManyToManyField(
        Category,
        related_name='products'
    )  # N:M

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# 🛒 Carrito
# =========================
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )  # 1:N

    products = models.ManyToManyField(
        Product,
        through='CartItem',
        related_name='carts'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user}"


# =========================
# 🧾 CartItem (tabla intermedia)
# =========================
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product} x {self.quantity}"
```

## 4 Admin de django
📁 store/admin.py
```python
from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_seller')
    list_filter = ('is_seller',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'owner')
    list_filter = ('categories',)
    search_fields = ('name',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
```

## 5 Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 6 Crear super useario
```bash
python manage.py createsuperuser
```

## 7 Ejecutar Servidor
```bash
python manage.py runserver
```
👉 Ir a:
```bash
http://127.0.0.1:8000/admin/
```