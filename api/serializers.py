from rest_framework import serializers
from .models import MedicineBase,User,MedStocks
from rest_framework.response import Response
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RegisterUser
#         fields = ['id', 'username', 'email', 'password'] 
        
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'confirm_pass': {'write_only': True}, # to make the password field hidden from users
#         }
        
        
#     def create(self, validated_data):
#         username = validated_data.get('username')
#         email  = validated_data.get('email')
#         password = validated_data.get('password')
#         if  password is not None:
#              user = RegisterUser(username=username, email=email)
#              user.set_password(password)
#              user.save()    
#              return user
#         else:
#             raise serializers.ValidationError({
#                     'error': 'Both passwords does not match',
#              }) 
 
# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=255)
#     class Meta:
#         model  = RegisterUser
#         fields = ['username', 'password' ]
   
class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']
    
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBase
        # fields = ['m_id','medicine_weight','created_at','updated_at']
        exclude = ['m_id','created_at','updated_at']
        
class MedStocksSerializer(serializers.ModelSerializer):
  class Meta:
    model = MedStocks
    exclude = ['med_id']        