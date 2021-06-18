from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('add', views.add),
    path('search', views.search),
    path('info/<int:customer_id>', views.customer_info),
    path('post-note', views.post_note),
    path('contact-history', views.contact_history),
    path('order-history', views.order_history),
]