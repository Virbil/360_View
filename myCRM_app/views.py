from django.contrib.messages.api import info
from myCRM_app.decorators import validate_request
from django.contrib import messages
from myCRM_app.models import *
from django.shortcuts import render, redirect
import datetime as dt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json

@validate_request
def home(request, logged_user):
    request.session['customer'] = 0

    context = {
        "user_info": logged_user,
        "searched_customers": Customer.objects.filter(id=request.session["customer"])
    }
    return render(request, "home.html", context)


def search(request, info_provided):
    request.session['customer'] = None
    searched_customers = []

    if request.method == "POST":
        if info_provided == 'email':
            searched_customers = Customer.objects.filter(email = request.POST['email'])

        elif info_provided == 'phone':
            searched_customers = Customer.objects.filter(phone_number = request.POST['phone_number'])
        
        else:
            customer = Customer.objects.filter(
                first_name = request.POST['first_name'].title(),
                last_name = request.POST['last_name'].title(),
                birthday = request.POST['birthday']
            )
            searched_customers = customer

        if searched_customers:
            customer_id = searched_customers[0].id
            request.session["customer"] = customer_id
        
            context = {
                'searched_customers': searched_customers
            }

            return render(request, 'customer-list.html', context)
        else:
            request.session["error_no_customer"] = "No customer exists. Please try again"
            return render(request, 'customer-list.html')


@validate_request
def maintain_users(request, logged_user):
    all_users = User.objects.all()

    context = {
        "user_info": logged_user,
        "all_users": all_users
    }
    return render(request, "maintenance.html", context)

def edit_user(request, user_id):
    user_to_edit = User.objects.get(id = user_id)
    user_to_edit.email = request.POST['email']
    user_to_edit.user_type = request.POST['user_type']
    user_to_edit.save()
    return redirect('/customer/maintenance')

def delete_user(request, user_id):
    user_to_delete = User.objects.get(id = user_id)
    all_users = User.objects.all()
    if len(all_users) > 1:
        user_to_delete.delete()
    else:
        print("There is only 1 user. Can't delete.")
    return redirect('/customer/maintenance')


def add_customer(request):

    if request.method == "POST":
        errors = Customer.objects.new_cust_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

        phone_number = request.POST['phone_number']
        if phone_number[:2] == "1-":
            phone_number = phone_number
        else:
            phone_number = f"1-{phone_number}"

        new_customer = Customer.objects.create(
            first_name = request.POST["first_name"].title(),
            last_name = request.POST["last_name"].title(),
            phone_number = phone_number,
            email = request.POST["email"],
            birthday = request.POST["birthday"]
        )
    return redirect(f'/customer/info/{new_customer.id}')


@validate_request
def customer_info(request, logged_user, customer_id):

    customer_id = customer_id

    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=customer_id),
        'orders': Order.objects.filter(customer = customer_id)
    }
    return render(request, 'cust-info.html', context)

@validate_request
def edit_customer_info(request, logged_user, customer_id):

    customer_id = customer_id
    customer_to_edit = Customer.objects.get(id = customer_id)

    phone_number = request.POST['phone_number']
    if phone_number[:2] == "1-":
        phone_number = phone_number
    else:
        phone_number = f"1-{phone_number}"
    
    if request.method == "POST":
        customer_to_edit.first_name = request.POST["first_name"].title()
        customer_to_edit.last_name = request.POST["last_name"].title()
        customer_to_edit.phone_number = phone_number
        customer_to_edit.email = request.POST["email"]
        customer_to_edit.birthday = request.POST["birthday"]
        customer_to_edit.save()

        return redirect(f'/customer/info/{customer_id}')

@validate_request
def contact_history(request, logged_user):
    customer = Customer.objects.get(id=request.session["customer"])
    notes_list = Note.objects.filter(customer=customer)

    page = request.GET.get('page', 1)
    paginator = Paginator(notes_list, 6)

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=request.session["customer"]),
        'notes': notes
    }
    return render(request, 'contact-history.html', context)

@validate_request
def post_note(request, logged_user):
    customer = request.session["customer"]
    if request.method == "POST":
        note = Note.objects.create(
            note = request.POST["note"],
            user = logged_user,
            customer = Customer.objects.get(id=customer)
        )
    return redirect('/customer/contact-history')

@validate_request
def order_history(request, logged_user):
    customer = request.session["customer"]
    orders_list = Order.objects.filter(customer=customer)

    all_products = Product.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(orders_list, 6)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=customer),
        'products': all_products,
        'orders': orders
    }
    return render(request, 'order-history.html', context)

@validate_request
def place_order(request, logged_user):
    customer = Customer.objects.get(id=request.session["customer"])

    # api call
    response = requests.get('https://fakestoreapi.com/products')

    all_products = json.loads(response.text)
    # json_formatted_str = json.dumps(all_products, indent=2)
    # for product in all_products:
    #     print(f"Title: {product['title']}")
    #     print(f"Description: {product['description']}")
    #     print(f"Price: {product['price']}")
    #     print(f"Image: {product['image']}")

    # If product doesn't exist, add to DB
    for product in all_products:
        try:
            new_product = Product.objects.get(id=product['id'])
        except:
            new_product = Product.objects.create(
                product_name = product['title'],
                description = product['description'],
                price = product['price'],
                product_image = product['image']
            )
            print(new_product.product_name)


    if request.method == "GET":
        customer = request.session["customer"]
        # all_products = Product.objects.all()
        context = {
            'user_info': logged_user,
            'customer': Customer.objects.get(id=customer),
            'products': all_products
        }
        return render(request, 'place-order.html', context)

    if request.method == "POST":
        products = request.POST.getlist('products')

        new_order = Order.objects.create(
            customer = customer
        )

        for product in products:
            new_order.products.add(Product.objects.get(id=product))

        return redirect('/customer/order-history')