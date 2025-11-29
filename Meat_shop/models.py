from django.db import models
from datetime import date
import uuid  # ← добавь это вверху, если используешь uuid в views (не в models)

# 1. Сначала Product
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('beef', 'Говядина'),
        ('lamb', 'Баранина'),
        ('chicken', 'Курица'),
    ]
    name = models.CharField('Название', max_length=100)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField('Описание', blank=True)
    price_per_kg = models.DecimalField('Цена за кг', max_digits=10, decimal_places=2, default=0.00)
    expiration_date = models.DateField('Срок годности', default=date.today)
    image = models.ImageField('Фото', upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} — {self.name} ({self.price_per_kg} руб/кг)"

# 2. Потом Cart
class Cart(models.Model):
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

# 3. Потом CartItem (уже может ссылаться на Cart и Product)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=3)

# 4. И только потом Order (если он использует Product — а он использует)
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта при получении'),
        ('online', 'Онлайн-оплата'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    customer_name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес')
    weight_kg = models.DecimalField('Количество (кг)', max_digits=6, decimal_places=3)
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_CHOICES, default='cash')
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)

    def __str__(self):
        return f"Заказ от {self.customer_name} ({self.phone})"