from django.urls import path
from .views import CustomerChangePasswordView, CustomerProfileView, CustomerRegistrationView, CustomerLoginView, CustomerPasswordResetEmailView, CustomerPasswordResetView
urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name = 'customer-register'),
    path('login/', CustomerLoginView.as_view(), name='customer-login'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('change-password/', CustomerChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', CustomerPasswordResetEmailView.as_view(), name='reset-password'),
    path('reset-password/<uid>/<token>/', CustomerPasswordResetView.as_view(), name='reset-password'),

]
