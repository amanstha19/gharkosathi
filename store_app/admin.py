from django.contrib import admin
from .models import *

class imagesTabularInline(admin.TabularInline):
    model = images

class tagTabularInline(admin.TabularInline):
    model = tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [imagesTabularInline, tagTabularInline]
    list_display = ('name', 'price', 'stock', 'status', 'added_date')
    list_filter = ('stock', 'status', 'added_date')
    search_fields = ('name', 'description')

admin.site.register(Categorie)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(images)
admin.site.register(tag)
admin.site.register(Filter_Price)
