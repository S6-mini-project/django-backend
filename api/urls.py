from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from requests import request
from .views import MedicineAPI

urlpatterns = [
    path('api/medicine',MedicineAPI.as_view())
]