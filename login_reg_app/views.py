from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
import datetime as dt
import bcrypt

def sign_in(request):
    return render(request, "sign-in.html")

def log_in(request):
    if request.method == "POST":
        errors = User.objects.sign_in_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        # LOGIN
        try:
            user = User.objects.filter(email = request.POST["email"])
            if user:
                logged_in_user = user[0]
                if bcrypt.checkpw(request.POST["password"].encode(), logged_in_user.password.encode()):
                    request.session['userid'] = logged_in_user.id
                    request.session['user'] = logged_in_user.first_name

                    return redirect('/customer')
                else:
                    print("Incorrect password")
        except:
            print("No email was found")
        
    return redirect('/')

def register(request):
    return render(request, "register.html")

def reg_me(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            birthday = dt.datetime.strptime(request.POST["birthday"], "%m/%d/%Y"),
            password = pw_hash
        )

        request.session["user"] = new_user.first_name
        request.session["userid"] = new_user.id
        return redirect('/customer')

def email(request):
    if request.method == "POST":
        found = False
        check_email = User.objects.filter(email=request.POST['email'])
        if check_email:
            found = True
        context = {
            "found": found
        }
    return render(request, 'email-snippet.html', context)

def success(request):
    context = {
        "user_info": User.objects.get(id=request.session["userid"])
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')