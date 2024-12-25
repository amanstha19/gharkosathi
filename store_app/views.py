from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from store_app.models import Product, Categorie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from cart.cart import Cart
from store_app.models import Order, Delivery, Wishlist, OrderItem
from django.contrib.auth import login
from django.http import HttpResponse


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'main/index.html', context)

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
    CATID = request.GET.get('category')
    if CATID:
        products =Product.objects.filter( categorie=CATID)
    else:
        products = Product.objects.all()



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


        if User.objects.filter(email=email).exists():
            return render(request, 'register/auth.html', {'error_message': 'Email address is already in use'})

        # Check if passwords match
        if pass1 != pass2:
            return render(request, 'register/auth.html', {'error_message': 'Passwords do not match'})

        # Set a default yedi not provided
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

def help_page(request):
    return render(request, 'main/help.html')


def detail_page(request):
    return render(request, 'main/detail.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def about_page(request):
    return render(request, 'main/about.html')


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
@login_required(login_url="/main/register/auth/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)

    # Calculate total price after removing the item
    total_price = calculate_total_price(cart)

    # Return JSON response with updated total price
    return JsonResponse({'total_price': total_price})


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
    cart = Cart(request)
    total_price = calculate_total_price(cart)  # Calculate total price
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total_price': total_price})


# Calculate total price based on items in the cart
def calculate_total_price(cart):
    total_price = 0
    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * item['quantity']
    return total_price


@login_required
def userprofile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    deliveries = Delivery.objects.filter(order__user=user)
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    context = {
        'user': user,
        'orders': orders,
        'deliveries': deliveries,
        'wishlist': wishlist,
    }

    return render(request, 'main/userprofile.html', context)


def checkout(request):
    if request.method == "POST":
        try:



            cart_items = Cart.objects.filter(user=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)



            # Render the checkout page with a thank you message, order ID, and total price
            return render(request, 'register/success.html', {'thank': True, 'id': order.id, 'total_price': total_price})

        except Exception as e:
            # Handle any errors that occur during form submission
            return render(request, 'register/checkout.html', {'error_message': str(e)})

    # Render the checkout page if the request method is not POST
    return render(request, 'register/checkout.html')
def update_total_price(request):
    # Check if the request is a POST request and has the 'HTTP_X_REQUESTED_WITH' header set to 'XMLHttpRequest'
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Calculate total price here
        cart = Cart(request)
        total_price = calculate_total_price(cart)

        return JsonResponse({'total_price': total_price})
    else:
        # Handle non-AJAX requests appropriately
        # For example, return a 404 Not Found response
        return JsonResponse({'error': 'Not Found'}, status=404)



def place_order(request):

    return HttpResponse("Order placed successfully")

from django.shortcuts import render


def remove_from_cart(request, product_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=product_id)  # Assuming you have a Product model
        cart.remove(product)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


def about(request):
    return render(request, 'main/about.html')



