# 🚀 SPRINT 1 — Setup + Modelado Base
## 🎯 Objetivo
Tener:
* Proyecto Django funcionando
* App store (tienda)
* Modelos con relaciones:
    - 1:N → Usuario → Producto
    - N:M → Producto ↔ Categoría
    - N:M → Carrito ↔ Producto (con CartItem)
* Admin operativo

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
AUTH_USER_MODEL = 'store.User'
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

# 🚀 SPRINT 2 — Autenticación + UI Base
## 🎯 Objetivo
* Registro, login, logout
* Layout base con Bootstrap 5.3
* Navbar dinámica (login / logout)
* Listado de productos (cards)
* Home pública

1. URLs del proyecto
📁 config/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]
```

2. URLs de la app
📁 crea el archivo urls.py en store/urls.py y agrega lo siguiente:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

3. Formularios
📁 crea el archivo forms.py en store/forms.py y agregua lo siguiente:
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_seller', 'password1', 'password2')
```

4. Vistas
📁 marketplace/views.py agrega lo siguiente:
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from .models import Product


def home(request):
    products = Product.objects.select_related('owner').prefetch_related('categories').all()
    return render(request, 'marketplace/home.html', {'products': products})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'marketplace/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'marketplace/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
```

5. Templates (Bootstrap 5.3)
📁 Crear la carpeta templates y dentro la carpeta store para agregar lo siguientes archivos de la Estructura que se muestra
```bash
templates/
 └── store/
     ├── base.html
     ├── home.html
     ├── login.html
     └── register.html
```

🧩 base.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Marketplace</title>

    <!-- Bootstrap 5.3 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="/">Marketplace</a>

    <div>
      {% if user.is_authenticated %}
        <span class="text-white me-3">Hola {{ user.username }}</span>
        <a href="{% url 'logout' %}" class="btn btn-outline-light btn-sm">Logout</a>
      {% else %}
        <a href="{% url 'login' %}" class="btn btn-outline-light btn-sm me-2">Login</a>
        <a href="{% url 'register' %}" class="btn btn-primary btn-sm">Registro</a>
      {% endif %}
    </div>
  </div>
</nav>

<div class="container mt-4">
    {% block content %}{% endblock %}
</div>

</body>
</html>
```

🏠 home.html
```bash
{% extends 'store/base.html' %}

{% block content %}

<h2 class="mb-4">Productos</h2>

<div class="row">
    {% for product in products %}
    <div class="col-md-4">
        <div class="card mb-4 shadow-sm">
            <div class="card-body">
                <h5>{{ product.name }}</h5>
                <p>{{ product.description|truncatechars:80 }}</p>

                <p><strong>$ {{ product.price }}</strong></p>

                <small class="text-muted">
                    Vendedor: {{ product.owner.username }}
                </small>

                <div class="mt-2">
                    {% for cat in product.categories.all %}
                        <span class="badge bg-secondary">{{ cat.name }}</span>
                    {% endfor %}
                </div>

            </div>
        </div>
    </div>
    {% empty %}
        <p>No hay productos aún.</p>
    {% endfor %}
</div>

{% endblock %}
```

🔐 login.html
```html
{% extends 'marketplace/base.html' %}

{% block content %}

<h2>Login</h2>

<form method="POST">
    {% csrf_token %}
    <input type="text" name="username" placeholder="Usuario" class="form-control mb-2">
    <input type="password" name="password" placeholder="Contraseña" class="form-control mb-2">

    <button class="btn btn-primary">Ingresar</button>
</form>

{% endblock %}
```

📝 register.html
```html
{% extends 'marketplace/base.html' %}

{% block content %}

<h2>Registro</h2>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}

    <button class="btn btn-success">Registrarse</button>
</form>

{% endblock %}
```

6. Ejecutar el proyecto
```bash
python manage.py runserver
```

🧪 7. Flujo de prueba
1. Ir a /register/
2. Crear usuario
3. Login automático
4. Ver productos en /
5. Logout desde navbar

✅ Resultado del Sprint 2
✔ Autenticación completa
✔ UI base profesional con Bootstrap
✔ Navbar dinámica
✔ Listado de productos
✔ Estructura lista para escalar
