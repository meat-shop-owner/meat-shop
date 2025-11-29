from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import uuid
from .models import Product, Order, Cart, CartItem

def get_cart_id(request):
    if 'cart_id' not in request.session:
        request.session['cart_id'] = str(uuid.uuid4())
    return request.session['cart_id']

def index(request):
    return render(request, 'index.html')

# --- Отдельные views для каждой категории ---
def beef_view(request):
    products = Product.objects.filter(category='beef')
    return render(request, 'beef.html', {'products': products})

def lamb_view(request):
    products = Product.objects.filter(category='lamb')
    return render(request, 'lamb.html', {'products': products})

def chicken_view(request):
    products = Product.objects.filter(category='chicken')
    return render(request, 'chicken.html', {'products': products})

# --- Корзина и заказ ---
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(session_id=cart_id)

    if request.method == 'POST':
        weight = request.POST.get('weight_kg')
        if weight:
            CartItem.objects.create(cart=cart, product=product, weight_kg=weight)
            messages.success(request, f'{product.name} добавлен в корзину!')
    return redirect('cart_view')

def cart_view(request):
    cart_id = get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(session_id=cart_id)
    items = cart.items.select_related('product')
    total_weight = sum(item.weight_kg for item in items)
    return render(request, 'cart.html', {'cart_items': items, 'total_weight': total_weight})

def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        messages.success(request, 'Товар удалён из корзины.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Товар не найден.')
    return redirect('cart_view')

def checkout(request):
    cart_id = get_cart_id(request)
    cart, _ = Cart.objects.get_or_create(session_id=cart_id)
    items = cart.items.select_related('product')

    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        phone = request.POST['phone']
        address = request.POST['address']
        payment_method = request.POST['payment_method']  # ← новый параметр

        for item in items:
            Order.objects.create(
                product=item.product,
                customer_name=customer_name,
                phone=phone,
                address=address,
                weight_kg=item.weight_kg,
                payment_method=payment_method  # ← сохраняем
            )
        cart.items.all().delete()
        messages.success(request, 'Ваш заказ принят! Мы скоро свяжемся с вами.')
        return redirect('index')

    return render(request, 'checkout.html', {'cart_items': items})