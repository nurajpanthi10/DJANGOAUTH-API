from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CustomerChangePasswordSerializer, CustomerLoginSerializer, CustomerPasswordResetEmailSerializers, CustomerProfileSerializer, CustomerRegistrationSerializer, CustomerPasswordResetSerializer
from django.contrib.auth import authenticate
from .renderers import CustomerRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_customer(customer):
  refresh = RefreshToken.for_user(customer)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


#Customer Registration View
class CustomerRegistrationView(APIView):
  renderer_classes = [CustomerRenderer]
  def post(self, request, format=None):
    serializer = CustomerRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    customer = serializer.save()
    token = get_tokens_for_customer(customer)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class CustomerLoginView(APIView):
  renderer_classes = [CustomerRenderer]
  def post(self, request, format=None):
    serializer = CustomerLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    customer = authenticate(email=email, password=password)
    if customer is not None:
      token = get_tokens_for_customer(customer)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class CustomerProfileView(APIView):
  renderer_classes = [CustomerRenderer]
  permission_classes = [IsAuthenticated]
  
  def get(self, request, format = None):
    serializer = CustomerProfileSerializer(request.user)
    return Response(serializer.data, status = status.HTTP_200_OK)


class CustomerChangePasswordView(APIView):
  renderer_classes = [CustomerRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = CustomerChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)


class CustomerPasswordResetEmailView(APIView):
    renderer_classes=[CustomerRenderer]

    def post(self, request, format=None):
      serializer = CustomerPasswordResetEmailSerializers(data = request.data)
      if serializer.is_valid(raise_exception=True):
        return Response({'msg': 'Password link send. Please check your email.'}, status=status.HTTP_200_OK)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerPasswordResetView(APIView):
  renderer_classes = [CustomerRenderer]

  def post(self, request, uid, token, format = None):
    serializer = CustomerPasswordResetSerializer(data = request.data, context = {'uid': uid, 'token' : token})
    if serializer.is_valid(raise_exception=True):
      return Response({'msg' : "Password Reset Successfull."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)