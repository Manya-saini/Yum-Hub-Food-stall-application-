from django.shortcuts import *
from .models import *
from django.http import *
from django.contrib.auth import authenticate, login as auth_login, logout
import json
import ast
from decimal import Decimal
from .backends import ProfileBackend
from django.contrib.auth.decorators import login_required
import base64
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')
    # return HttpResponse("This is index")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile = Profile.objects.get(user=user)
            if profile.user_type == 'admin':
                auth_login(request, user)
                return redirect('admin_dashboard')
            else:
                auth_login(request, user)
                return redirect('menu')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        # Create a new User instance
        user = User.objects.create_user(username=username, password=password)
        
        # Create a new Profile instance and link it to the user
        profile = Profile.objects.create(name=name, phone=phone, user_type=user_type, username=username, user=user)

        # Redirect to the login page
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def menu(request):
    dishes = Dish.objects.all()  # Fetch all dishes
    for dish in dishes:
        with open(dish.image.path, "rb") as img_file:
            dish.image_data = base64.b64encode(img_file.read()).decode('utf-8')
    return render(request, 'menu.html', {'dishes': dishes})

@login_required
def checkout(request):
    if request.method == 'POST':
        total_orders = {}
        total_amount = 0
        dishes = Dish.objects.all()

        for dish in dishes:
            quantity = int(request.POST.get(f'dish_{dish.id}'))
            if quantity > 0:
                total_orders[dish.id] = quantity
                total_amount += quantity * dish.price

        processed_orders = []
        for dish_id, quantity in total_orders.items():
            dish = Dish.objects.get(pk=dish_id)
            processed_orders.append({'name': dish.name, 'price': dish.price, 'quantity': quantity})
            
        return render(request, 'checkout.html', {'total_orders': total_orders, 'total_amount': total_amount, 'processed_orders': processed_orders})

    return redirect('menu')  # Redirect to menu if not a POST request



@login_required
def payment(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')
        processed_orders = request.POST.getlist('processed_orders[]')
        tax = float(total_amount)*0.10
        total=float(total_amount)+tax
        # Process the payment and generate the bill using the received data

        return render(request, 'payment.html', {'total_amount': total_amount, 'processed_orders': processed_orders,'total':total})

    total_amount=None
    processed_orders=[]
    total = 0
    return render(request, 'payment.html', {'total_amount': total_amount,'processed_orders':processed_orders,'total':total})


    # Redirect to menu page if not a POST request
    return redirect('menu')

@login_required
def bill(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')
        processed_orders = request.POST.getlist('processed_orders[]')
        tax = float(total_amount)*0.10
        total=float(total_amount)+tax
        # for order in processed_orders:
        #     o_total=order.price*order.quantity
        #     order.append(o_total)
        def preprocess_order_string(order_str):
            return order_str.replace("Decimal(", "").replace(")", "")

        # Process the payment and generate the bill using the received data
        processed_orders_dicts = []
        for order_str in processed_orders:
            order_str = preprocess_order_string(order_str)
            order_dict = ast.literal_eval(order_str)
            order_dict['o_total']=float(order_dict['quantity']*float(order_dict['price']))
            order_dict['price'] = Decimal(order_dict['price'])  # Convert price to Decimal
            processed_orders_dicts.append(order_dict)

        return render(request, 'bill.html', {'total_amount': total_amount, 'processed_orders': processed_orders_dicts,'tax':tax,'total':total})

    total_amount=None
    processed_orders=[]
    tax=None
    total = None
    return render(request, 'bill.html', {'total_amount': total_amount, 'processed_orders': processed_orders,'tax':tax,'total':total})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.method == 'POST':
        dish_name = request.POST.get('dish_name')
        dish_description = request.POST.get('dish_description')
        dish_image = request.FILES.get('dish_image')
        dish_price = request.POST.get('dish_price')

        # Create and save the new dish
        new_dish = Dish(name=dish_name, image=dish_image, price=dish_price, quantity = 0)
        new_dish.save()

        # Add success message
        messages.success(request, 'Dish added successfully!')

        # Redirect to the admin dashboard page
        return redirect('admin_dashboard')
    
    return render(request, 'admin_dashboard.html')

# @login_required
# def progress(request):
#     orders = Order.objects.filter(user__vendor=request.user)  # Filter orders for this vendor
#     dish_sales = {}  # Dictionary to store data
#     total_revenue = 0
#     for order in orders:
#       for item in order.items.all():
#         dish_sales[item.dish.name] = dish_sales.get(item.dish.name, {'quantity': 0, 'revenue': 0})
#         dish_sales[item.dish.name]['quantity'] += item.quantity
#         dish_sales[item.dish.name]['revenue'] += item.dish.price * item.quantity
#         total_revenue += item.dish.price * item.quantity
#     return render(request, 'vendor.html', {'sales_data': dish_sales, 'total_revenue': total_revenue})

