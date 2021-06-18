from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('log-in', views.log_in),
    path('register', views.register),
    path('reg-me', views.reg_me),
    path('email', views.email),
    path('success', views.success),
    path('logout', views.logout),
]