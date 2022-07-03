from importlib.resources import read_binary
from turtle import update
from rest_framework import serializers
from .models import MedicineBase,RegisterUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['id', 'name', 'email', 'password','confirm_password'] 
        
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_pass': {'write_only': True}, # to make the password field hidden from users
        }
        
        
    def create(self, validated_data):
        password = validated_data['password',None]
        confirm_pass = validated_data['confirm_pass',None]
        instance = self.Meta.model(**validated_data)
        if password is not None and password==confirm_pass:
            instance.set_password(password)
        instance.save()    
        return instance

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBase
        # fields = ['m_id','medicine_weight','created_at','updated_at']
        exclude = ('m_id','created_at','updated_at')