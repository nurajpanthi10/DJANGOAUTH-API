from django.urls import path
from .views import CustomerRegistrationView, CustomerLoginView
urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name = 'customer-register'),
    path('login/', CustomerLoginView.as_view(), name='customer-login')
]
