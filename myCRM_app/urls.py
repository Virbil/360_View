from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('add', views.add_customer),
    path('search', views.search),
    # path("ajax_search", views.autocomplete_model, name='autocomplete_model'),
    path('info/<int:customer_id>', views.customer_info),
    path('edit-info/<int:customer_id>', views.edit_customer_info),
    path('post-note', views.post_note),
    path('contact-history', views.contact_history),
    path('order-history', views.order_history),
    path('place-order', views.place_order),
]