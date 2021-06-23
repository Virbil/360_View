from django.db import models
from django.db import models
from login_reg_app.models import User
import datetime as dt
import re

class Customer_Manager(models.Manager):
    def age_of_user(self, birth_year):
        date_today = dt.date.today().year
        age = date_today - birth_year
        
        return int(age)

    def new_cust_validator(self, post_data):
        errors = {}

        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        
        if len(post_data["birthday"]) < 1:
            errors["birthday"] = "Please select or enter a birthday"
        if post_data["birthday"].isalpha() == True:
            errors["birthday"] = "Birthday must be a valid date"
        if len(post_data["birthday"]) > 0:
            date_entered = post_data["birthday"]
            birthday = dt.datetime.strptime(date_entered, '%Y-%m-%d')

            if birthday > dt.datetime.now():
                errors["birthday"] = 'Birthday should be in the past'
            if self.age_of_user(birthday.year) < 13:
                errors["birthday"] = "Must be 13 years or older to Register"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):           
            errors['email'] = "Invalid email address!"

        email_match = Customer.objects.filter(email=post_data['email'])
        if len(email_match) > 0:
            errors['email'] = "This email has already been taken!"

        phone_match = Customer.objects.filter(phone_number=post_data['phone_number'])
        if len(phone_match) > 0:
            errors['phone_number'] = "This phone number has already been taken!"

        return errors

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Customer_Manager()

class Note(models.Model):
    note = models.TextField()
    user = models.ForeignKey(User, related_name="note_by_user", on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="note_for_customer", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name="customer_order", on_delete = models.CASCADE)  
    products = models.ManyToManyField(Product, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
