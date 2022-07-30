from this import s
from rest_framework import status, serializers
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from requests import request
from .serializers import MedicineSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer, MedStocksSerializer
from django.http import HttpResponse, JsonResponse, Http404
from .models import MedicineBase
from .models import MedStocks as MedStocksModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from .renderers import UserRenderer
# Create your views here.


# manual tokens

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MedicineAPI(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MedicineBase.objects.get(pk=pk)
        except MedicineBase.DoesNotExist:
            raise Http404

    def get(self, request):
        medicine = MedicineBase.objects.all()
        serializer = MedicineSerializer(medicine, many=True)
        if request.method == 'GET':

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=400)

    def post(self, request):
        if request.method == 'POST':
            try:
                serializer = MedicineSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
        else:
            return JsonResponse(serializer.errors, status=400)


class MedStocks(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        if request.method == 'POST':
            try:
                print(request.data)
                serializer = MedStocksSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
            else:
                return JsonResponse(serializer.errors, status=400)
    
    def get(self, request):
        med = MedStocksModel.objects.all()
        serializer = MedStocksSerializer(med, many=True)
        if request.method == 'GET':
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=400)        


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


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
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


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
            refresh_token = request.data['refresh_token']
            # print(request.data['refresh_token'])
            # # #takes the refresh token from request

            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "logout successfull!"
            })
        # moves token from outstanding tokens to blacklisted tokens
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
