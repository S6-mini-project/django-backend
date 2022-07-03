from rest_framework import status
from rest_framework.decorators import api_view,APIView
from rest_framework.response import Response
from requests import request
from .serializers import MedicineSerializer
from django.http import HttpResponse, JsonResponse,Http404
from .models import MedicineBase

# Create your views here.
class MedicineAPI(APIView):
    # authentication_classes = [JWTAuthentication]
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