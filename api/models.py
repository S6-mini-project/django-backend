from typing import OrderedDict
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin



# Create your models here.
# class RegisterUser(AbstractUser):
#     username= models.CharField(max_length=255, unique=True)
#     email= models.EmailField(max_length=255, unique=True)
#     password= models.CharField(max_length=255)
    
#     USERNAME_FIELD='username'
#     REQUIRED_FIELDS =['password' ] #


class MedicineBase(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    # medicine_weight = models.CharField(max_length=20, help_text='Enter field documentation')
    m_id = models.AutoField(primary_key=True)
    medicine_weight = models.CharField(max_length=20)
    medicine_name = models.CharField(max_length=255,default=None)
    minimum_stock = models.CharField(max_length=255,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    

    # Metadata
    class Meta:
        ordering = ['created_at']

    # Methods
    # def get_absolute_url(self):
    #     """Returns the URL to access a particular instance of MyModelName."""
    #     return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.medicine_weight
    # def __str__(self):
    #     """String for representing the Model object."""
    #     return f'{self.id} ({self.book.title})'
#sample data
# record = MedicineBase(m_id=1,medicine_weight="30")
# record.save()    

class MedStocks(models.Model):
    m_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=255)
    minimum_stock = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['m_id']