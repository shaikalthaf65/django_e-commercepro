from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Avg, Count
from .models import Product, Customer, Order, Rating


def cart_count(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())


def index(request):
    return redirect('home')


def home(request):
    return render(request, 'home.html', {
        'cart_count': cart_count(request)
    })


def register(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please enter email and password")
            return redirect('register')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "User already exists")
            return redirect('register')

        Customer.objects.create(
            email=email,
            password=password
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Customer.objects.filter(email=email, password=password).first()

        if user:
            request.session['user'] = user.email
            return redirect('products')
        else:
            messages.error(request, "User does not exist")

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect("login")


def products(request):

    if 'user' not in request.session:
        return redirect('login')

    query = request.GET.get('search')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    for p in products:

        ratings = Rating.objects.filter(product=p)

        avg = ratings.aggregate(Avg('stars'))['stars__avg']
        count = ratings.aggregate(Count('stars'))['stars__count']

        p.avg_rating = round(avg, 1) if avg else 0
        p.total_ratings = count

    return render(request, 'product.html', {
        'products': products,
        'cart_count': cart_count(request),
        'query': query
    })


def add_to_cart(request, pid):

    cart = request.session.get('cart', {})
    pid = str(pid)

    cart[pid] = cart.get(pid, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('products')


def increase_qty(request, pid):

    cart = request.session.get('cart', {})
    pid = str(pid)

    if pid in cart:
        cart[pid] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_qty(request, pid):

    cart = request.session.get('cart', {})
    pid = str(pid)

    if pid in cart:

        cart[pid] -= 1

        if cart[pid] <= 0:
            del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):

    cart = request.session.get('cart', {})
    cart_products = []
    total = 0

    for pid, qty in cart.items():

        product = Product.objects.filter(id=pid).first()

        if not product:
            continue

        subtotal = product.price * qty
        total += subtotal

        cart_products.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'qty': qty,
            'subtotal': subtotal,
            'image': product.image
        })

    return render(request, 'cart.html', {
        'cart_products': cart_products,
        'total': total,
        'cart_count': cart_count(request)
    })


def remove_item(request, pid):

    cart = request.session.get('cart', {})
    pid = str(pid)

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    if not cart:
        return redirect('products')

    return redirect('cart')


def payment(request):

    cart = request.session.get('cart', {})
    cart_products = []
    total = 0

    for pid, qty in cart.items():

        product = Product.objects.filter(id=pid).first()

        if not product:
            continue

        subtotal = product.price * qty
        total += subtotal

        cart_products.append({
            'name': product.name,
            'image': product.image,
            'subtotal': subtotal
        })

    return render(request, 'payment.html', {
        'cart_products': cart_products,
        'total': total
    })


def pay(request):

    user_email = request.session.get('user')
    cart = request.session.get('cart', {})

    if user_email:

        customer = Customer.objects.get(email=user_email)

        for pid, qty in cart.items():

            product = Product.objects.filter(id=pid).first()

            if not product:
                continue

            Order.objects.create(
                customer=customer,
                product=product,
                quantity=qty,
                total_price=product.price * qty
            )

        send_mail(
            subject="Order Confirmation",
            message="Your order has been placed successfully",
            from_email=None,
            recipient_list=[user_email]
        )

    request.session.pop('cart', None)

    messages.success(request, "Order placed successfully")

    return redirect("products")


def order_history(request):

    if 'user' not in request.session:
        return redirect('login')

    user_email = request.session.get('user')

    customer = Customer.objects.get(email=user_email)

    orders = Order.objects.filter(customer=customer)

    return render(request, 'orders.html', {
        'orders': orders
    })


def add_rating(request, pid):

    if 'user' not in request.session:
        return redirect('login')

    if request.method == "POST":

        stars = request.POST.get('stars')

        if not stars:
            return redirect('products')

        user_email = request.session.get('user')

        customer = Customer.objects.get(email=user_email)

        product = Product.objects.get(id=pid)

        existing_rating = Rating.objects.filter(
            customer=customer,
            product=product
        ).first()

        if existing_rating:
            existing_rating.stars = stars
            existing_rating.save()
        else:
            Rating.objects.create(
                product=product,
                customer=customer,
                stars=stars
            )

    return redirect('products')