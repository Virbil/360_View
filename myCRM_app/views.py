from django.contrib.messages.api import info
from myCRM_app.decorators import validate_request
from django.contrib import messages
from myCRM_app.models import *
from django.shortcuts import render, redirect, HttpResponse
import datetime as dt
import json

@validate_request
def home(request, logged_user):
    if 'customer' not in request.session:
        request.session['customer'] = 0

    context = {
        "user_info": logged_user,
        "searched_customers": Customer.objects.filter(id=request.session["customer"])
    }
    return render(request, "home.html", context)


def search(request, info_provided):
    request.session['customer'] = None

    if request.method == "POST":
        if info_provided == 'email':
            searched_customer = Customer.objects.filter(email=request.POST['email'])
        elif info_provided == 'phone':
            searched_customer = Customer.objects.filter(phone_number=request.POST['phone_number'])
        
            # customer_fname = Customer.objects.get(first_name=request.POST["first_name"])
            # customer_lname = Customer.objects.get(last_name=request.POST["last_name"])
            # customer_birth = Customer.objects.get(birthday=request.POST["birthday"])
            # searched_customer = Customer.objects.filter(customer=customer_fname).filter(customer=customer_lname).filter(customer=customer_birth)


        if searched_customer:
            customer_id = searched_customer[0].id
            request.session["customer"] = customer_id
        
        context = {
            'searched_customers': searched_customer
        }

        return render(request, 'customer-list.html', context)

    else:
        return redirect('/customer/register')


def autocomplete_model(request):
    if request.method == "GET":
        q = request.GET.get('term', '').capitalize()
        search_qs = Customer.objects.filter(email__startswith=q)
        results = []
        for r in search_qs[0:10]:
            results.append(r.email)

        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@validate_request
def register(request, logged_user):

    context = {
        "user_info": logged_user
    }

    return render(request, "add-customer.html", context)

def add_customer(request):

    if request.method == "POST":
        errors = Customer.objects.new_cust_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/customer/register')

        new_customer = Customer.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            phone_number = request.POST["phone_number"],
            email = request.POST["email"],
            birthday = dt.datetime.strptime(request.POST["birthday"], "%m/%d/%Y")
        )
    return redirect('/customer')

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
    
    if request.method == "POST":
        customer_to_edit.first_name = request.POST["first_name"]
        customer_to_edit.last_name = request.POST["last_name"]
        customer_to_edit.phone_number = request.POST["phone_number"]
        customer_to_edit.email = request.POST["email"]
        customer_to_edit.birthday = request.POST["birthday"]
        customer_to_edit.save()

        return redirect(f'/customer/info/{customer_id}')

@validate_request
def contact_history(request, logged_user):
    customer = Customer.objects.get(id=request.session["customer"])

    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=request.session["customer"]),
        'notes': Note.objects.filter(customer=customer)
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
    all_products = Product.objects.all()
    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=customer),
        'products': all_products,
        'orders': Order.objects.filter(customer=customer)
    }
    return render(request, 'order-history.html', context)

@validate_request
def place_order(request, logged_user):
    customer = Customer.objects.get(id=request.session["customer"])
    products = request.POST.getlist('products')

    if request.method == "GET":
        customer = request.session["customer"]
        all_products = Product.objects.all()
        context = {
            'user_info': logged_user,
            'customer': Customer.objects.get(id=customer),
            'products': all_products
        }
        return render(request, 'place-order.html', context)

    if request.method == "POST":
        new_order = Order.objects.create(
            customer = customer
        )
        for product in products:
            new_order.products.add(Product.objects.get(id=product))
        return redirect('/customer/order-history')