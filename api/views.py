from rest_framework import status
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
from requests import request
from .serializers import MedicineSerializer,UserSerializer
from django.http import HttpResponse, JsonResponse,Http404
from .models import MedicineBase,RegisterUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
class MedicineAPI(APIView):
    authentication_classes = [JWTAuthentication]
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
class RegisterAPIView(APIView):
    def post(self, request):
        print(request.data['confirm_password'])
        if request.data['confirm_password'] == request.data['password']:
            serializer = UserSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })
        else:
            return Response({ 'error' : 'passwords do not match! ' })    
           