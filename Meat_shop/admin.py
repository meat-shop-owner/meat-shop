from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_kg', 'expiration_date', 'image_tag')
    list_filter = ('category', 'expiration_date')
    search_fields = ('name',)
    fields = ('name', 'category', 'description', 'price_per_kg', 'expiration_date', 'image')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="border-radius:4px;" />'
        return "Нет фото"
    image_tag.short_description = 'Фото'
    image_tag.allow_tags = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'product', 'weight_kg', 'payment_method', 'address', 'created_at')
    list_filter = ('product__category', 'payment_method', 'created_at')
    search_fields = ('customer_name', 'phone', 'product__name')
    list_display_links = ('customer_name',)

    # Добавим колонку категории для удобства
    def product_category(self, obj):
        return dict(Order._meta.get_field('product').related_model.CATEGORY_CHOICES).get(obj.product.category)
    product_category.short_description = 'Категория'