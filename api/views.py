from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from requests import request
from .serializers import MedicineSerializer
from django.http import HttpResponse, JsonResponse
from .models import MedicineBase

# Create your views here.
@api_view()
def home(request):
    # if request.method == 'GET':
    return Response(
        {
            "status": "ok",
            "message" :"it is a GET request"
        }
    )
    # else: 
    #     return Response({"message": "it is not a GET request"})


# elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

#api to retrieve the medicine weights
# record = MedicineBase(m_id=1,medicine_weight="30")
# record.save() 
@api_view(['GET'])
def get_med_weights(request):
    # print(repr(serializer))
    medicine = MedicineBase.objects.all()
    serializer = MedicineSerializer(medicine,many=True)
    print(serializer.data)
    if request.method == 'GET': 
        return Response(
            {
                "status": "weight request successful",
                "message": serializer.data,
            }
        )        
    else:
        return JsonResponse(serializer.errors, status=400)
            
@api_view(['POST'])
def post_med_weights(request):
    if request.method == 'POST':
        try:
            data = request.data
            serializer = MedicineSerializer(data=data)
            if serializer.is_valid():
                serializer.save() 
                return Response (
                {
                "status": "weight added to the database",
                "message": serializer.data,
                }   )
        except Exception as e:
            print(e)        
    else:
        return JsonResponse(serializer.errors, status=400)
                                        