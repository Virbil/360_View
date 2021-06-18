from myCRM_app.models import *
from django.shortcuts import render, redirect
import datetime as dt

def home(request):
    logged_user = User.objects.get(id=request.session["userid"])
    if 'customer' not in request.session:
        request.session['customer'] = 0

    context = {
        "user_info": logged_user,
        "searched_customers": Customer.objects.filter(id=request.session["customer"])
    }
    return render(request, "home.html", context)

def search(request):
    request.session['customer'] = None
    logged_user = User.objects.get(id=request.session["userid"])

    if request.method == "POST":
        searched_customer = Customer.objects.filter(email=request.POST["email"])
        if searched_customer:
            customer_id = searched_customer[0].id
            request.session["customer"] = customer_id
        else:
            return redirect('/customer/register')
    return redirect('/customer')

def register(request):
    return render(request, "add-customer.html")

def add(request):
    if request.method == "POST":
    # errors = User.objects.reg_validator(request.POST)

    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('/register')

        new_customer = Customer.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            phone_number = request.POST["phone_number"],
            email = request.POST["email"],
            birthday = dt.datetime.strptime(request.POST["birthday"], "%m/%d/%Y")
        )
    return redirect('/customer')

def customer_info(request, customer_id):
    logged_user = User.objects.get(id=request.session["userid"])
    customer_id = customer_id
    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=customer_id)
    }
    return render(request, 'cust-info.html', context)

def contact_history(request):
    logged_user = User.objects.get(id=request.session["userid"])
    customer = request.session["customer"]
    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=customer),
        'notes': Note.objects.filter(user=logged_user)
    }
    return render(request, 'contact-history.html', context)

def post_note(request):
    logged_user = User.objects.get(id=request.session["userid"])
    customer = request.session["customer"]
    if request.method == "POST":
        note = Note.objects.create(
            note = request.POST["note"],
            user = logged_user,
            customer = Customer.objects.get(id=customer)
        )
    return redirect('/customer/contact-history')

def order_history(request):
    logged_user = User.objects.get(id=request.session["userid"])
    customer = request.session["customer"]
    print(customer)
    context = {
        'user_info': logged_user,
        'customer': Customer.objects.get(id=customer),
        'orders': Order.objects.filter(customer=customer)
    }
    return render(request, 'order-history.html', context)