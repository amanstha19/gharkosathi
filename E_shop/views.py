from django.views import View
from django.shortcuts import render, redirect
from store_app.models import Product
from django.contrib.auth.models import User

def BASE(request):
    return render(request, 'main/base.html')

def HOME(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'main/index.html', context)

def product(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'main/product.html', context)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 =  request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()

        return redirect('home')

    return render(request, 'register/auth.html')

class AuthView(View):
    def get(self, request):
        # Your view logic here
        return render(request, 'register/auth.html')
