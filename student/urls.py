"""
App-level URL configuration.
Maps URLs to view functions for all student modules.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('academics/', views.academics, name='academics'),
    path('attendance/', views.attendance, name='attendance'),
    path('fee/', views.fee, name='fee'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('make-payment/<int:fee_id>/', views.make_payment, name='make_payment'),
    path('feedback/', views.feedback, name='feedback'),
]
