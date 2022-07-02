from importlib.resources import read_binary
from turtle import update
from rest_framework import serializers
from .models import MedicineBase

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBase
        # fields = ['m_id','medicine_weight','created_at','updated_at']
        exclude = ('m_id','created_at','updated_at')