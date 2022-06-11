from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CustomerLoginSerializer, CustomerRegistrationSerializer
from django.contrib.auth import authenticate
from .renderers import CustomerRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class CustomerRegistrationView(APIView):
  renderer_classes = [CustomerRenderer]
  def post(self, request, format=None):
    serializer = CustomerRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class CustomerLoginView(APIView):
  renderer_classes = [CustomerRenderer]
  def post(self, request, format=None):
    serializer = CustomerLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
