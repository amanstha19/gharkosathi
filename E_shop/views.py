from django.shortcuts import render, redirect
from store_app.models import Product

def BASE(request):
    return render(request, 'main/base.html')

def HOME(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'main/index.html', context)
