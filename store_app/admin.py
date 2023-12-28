from django.contrib import admin
from .models import *
# Register your models here.

class imagesTabularInline(admin.TabularInline):
    model = images

class tagTabularInline(admin.TabularInline):
    model = tag
class ProductAdmin(admin.ModelAdmin):
    inlines = [imagesTabularInline, tagTabularInline]
admin.site.register(Categorie)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(images)
admin.site.register(tag)
admin.site.register(Filter_Price)
