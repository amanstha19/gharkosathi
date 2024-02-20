from django.contrib import admin
from .models import *

class imagesTabularInline(admin.TabularInline):
    model = images

class tagTabularInline(admin.TabularInline):
    model = tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [imagesTabularInline, tagTabularInline]
    list_display = ('name', 'price', 'stock',  'added_date')
    list_filter = ('stock', 'added_date')
    search_fields = ('name', 'description')


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username')
    inlines = [OrderItemInline]

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')
    search_fields = ('order__id',)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')




admin.site.register(Categorie)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(images)
admin.site.register(tag)
admin.site.register(Filter_Price)
admin.site.register(Order, OrderAdmin)
