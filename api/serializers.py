from importlib.resources import read_binary
from turtle import update
from click import confirm
from rest_framework import serializers
from .models import MedicineBase,RegisterUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['id', 'username', 'email', 'password'] 
        
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_pass': {'write_only': True}, # to make the password field hidden from users
        }
        
        
    def create(self, validated_data):
        username = validated_data.get('username')
        email  = validated_data.get('email')
        password = validated_data.get('password')
        # instance = self.Meta.model(**validated_data)
        if  password is not None:
             user = RegisterUser(username=username, email=email)
             user.set_password(password)
             user.save()    
             return user
        else:
            raise serializers.ValidationError({
                    'error': 'Both passwords does not match',
             }) 

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBase
        # fields = ['m_id','medicine_weight','created_at','updated_at']
        exclude = ('m_id','created_at','updated_at')