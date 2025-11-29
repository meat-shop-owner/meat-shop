from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/beef/', views.beef_view, name='beef'),
    path('category/lamb/', views.lamb_view, name='lamb'),
    path('category/chicken/', views.chicken_view, name='chicken'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
]