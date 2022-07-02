from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from requests import request
from .views import home,get_med_weights

urlpatterns = [
    path('',home,name='home'),
    path('get_med_weights/',get_med_weights,name='get_med_weights')
]