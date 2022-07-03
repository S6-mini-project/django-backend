from django.contrib import admin
from .models import MedicineBase,RegisterUser

# Register your models here.
# admin.site.register(MedicineBase)

# Define the admin class
class MedicineAdmin(admin.ModelAdmin):
    # pass
    list_display = ('m_id', 'medicine_weight', 'created_at','updated_at')
    fields = [('m_id', 'medicine_weight', 'created_at','updated_at')]
# Register the admin class with the associated model
admin.site.register(MedicineBase, MedicineAdmin)

class RegisterAdmin(admin.ModelAdmin):
    # pass
    list_display = ('id','username','email', 'password')
    fields = [('id','username', 'email' , 'password')]
# Register the admin class with the associated model
admin.site.register(RegisterUser, RegisterAdmin)