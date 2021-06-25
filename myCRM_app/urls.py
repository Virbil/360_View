from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add', views.add_customer),
    path('maintenance', views.maintain_users),
    path('users/<int:user_id>/edit', views.edit_user, name="edit_user_info"),
    path('users/<int:user_id>/delete', views.delete_user, name="delete_user"),
    path('search/<str:info_provided>', views.search),
    path('info/<int:customer_id>', views.customer_info),
    path('edit-info/<int:customer_id>', views.edit_customer_info),
    path('post-note', views.post_note),
    path('contact-history', views.contact_history),
    path('order-history', views.order_history),
    path('place-order', views.place_order),
]