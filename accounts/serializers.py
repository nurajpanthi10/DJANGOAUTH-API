from ast import Pass
from pyexpat import model
from django.forms import ValidationError
from rest_framework import serializers
from .models import Customer
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomerRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = Customer
    fields=['email', 'name', 'password', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return Customer.objects.create_user(**validate_data)

class CustomerLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = Customer
    fields = ['email', 'password']


class CustomerProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ['id', 'email', 'name']


class CustomerChangePasswordSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    model = Customer
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2 :
      raise serializers.ValidationError("Password and Confirm Password doesn't match.")
    user.set_password(password)
    user.save()
    return attrs

class CustomerPasswordResetEmailSerializers(serializers.Serializer):
  email = serializers.EmailField(max_length=255)

  class Meta:
    model = Customer
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if Customer.objects.filter(email=email).exists():
      user = Customer.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/customer/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+ link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      # Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')


class CustomerPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  
  class Meta:
    model = Customer
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2 :
        raise serializers.ValidationError("Password and Confirm Password doesn't match.")
      id = smart_str(urlsafe_base64_decode(uid))
      customer = Customer.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(customer, token):
        raise ValidationError('Token is not valid or expired.')
      customer.set_password(password)
      customer.save()
      return attrs

    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(customer, token)
      return ValidationError("Token is not Valid or Expired.")
