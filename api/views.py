
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
from requests import request
from .serializers import  MedicineSerializer,UserLoginSerializer,UserProfileSerializer,UserRegistrationSerializer
from django.http import HttpResponse, JsonResponse,Http404
from .models import MedicineBase,User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,logout
from .renderers import UserRenderer
# Create your views here.


#manual tokens

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class MedicineAPI(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return MedicineBase.objects.get(pk=pk)
        except MedicineBase.DoesNotExist:
            raise Http404

    def get(self, request):
        medicine = MedicineBase.objects.all()
        serializer = MedicineSerializer(medicine, many=True)
        if request.method == 'GET':
            return Response(
                {
                    "status": "weight request successful",
                    "message": serializer.data,
                }
            )
        else:
            return JsonResponse(serializer.errors, status=400)

    def post(self, request):
        if request.method == 'POST':
            try:
                serializer = MedicineSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "status": "weight added to the database",
                            "message": serializer.data,
                        })
            except Exception as e:
                print(e)
        else:
            return JsonResponse(serializer.errors, status=400)
        
 #user register api
# class RegisterAPIView(APIView):
#     def post(self, request):
#         print(request.data['confirm_password'])
#         if request.data['confirm_password'] == request.data['password']:
#             serializer = UserSerializer(data = request.data)
#             serializer.is_valid(raise_exception=True)
#             user = serializer.save()
#             token = get_tokens_for_user(user)
#             return Response({
#                 "user": serializer.data,
#                 "token": token,
#                 "message": "User Created Successfully.  Now perform Login to get your token",
#             })
#         else:
#             return Response({ 'error' : 'passwords do not match! ' })    
 
 
#  #login api
# class LoginAPIView(APIView): 
#     def post(self, request):      
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             username = serializer.data.get('username')
#             password = serializer.data.get('password') 
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 token = get_tokens_for_user(user)
#                 return Response({
#                     'message': 'Login successful!', 
#                      'token': token
#                 })
#             else:
#                 return Response({'errors': 'Login failed! username or  password incorrect!',status:status.HTTP_404_NOT_FOUND })
#         return Response( serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView): 
    renderer_classes = [UserRenderer] 
    def post(self, request):
        try:
            logout(request)
            refresh_token = request.data.get('refresh_token') #takes the refresh token from request
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "logout successfull!"
            })
        #moves token from outstanding tokens to blacklisted tokens
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            