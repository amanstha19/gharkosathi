from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from store_app.models import Product, Categorie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from cart.cart import Cart


class AuthView(View):
    def get(self, request):
        return render(request, 'register/auth.html')


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
    categories = Categorie.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/product.html', context)


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register/auth.html', {'error_message': 'Email address is already in use'})

        # Check if passwords match
        if pass1 != pass2:
            return render(request, 'register/auth.html', {'error_message': 'Passwords do not match'})

        # Set a default username if not provided
        if not username:
            username = email.split('@')[0]

        # Create a new user
        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()

        return redirect('register')

    return render(request, 'register/auth.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'register/auth.html', {'error_message': 'Invalid login credentials'})


def user_logout(request):
    logout(request)
    return redirect('home')


def search(request):
    query = request.GET.get('search')
    products = Product.objects.filter(name__icontains=query)

    context = {
        'products': products,
    }

    return render(request, 'main/search.html', context)


@login_required(login_url="/main/register/auth/")
def cart_add(request, product_id):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.add(product=product)

        # Return JSON response indicating success
        return JsonResponse({'success': True})
    else:
        return redirect("home")


@login_required(login_url="/main/register/auth/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/main/register/auth/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/main/register/auth/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/main/register/auth/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/main/register/auth/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
