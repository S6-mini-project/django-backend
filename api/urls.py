from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from requests import request
from .views import MedicineAPI,UserRegistrationView, UserLoginView, UserProfileView,LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('api/register',UserRegistrationView.as_view()),
    path('api/login',UserLoginView.as_view()),
    path('api/profile', UserProfileView.as_view(), name='profile'),
    path('api/logout', LogoutView.as_view()),
    path('api/medicine',MedicineAPI.as_view())
]