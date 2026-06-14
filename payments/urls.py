from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('verify/', views.payment_verify, name='payment_verify'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('webhook/', views.razorpay_webhook, name='razorpay_webhook'),
]
