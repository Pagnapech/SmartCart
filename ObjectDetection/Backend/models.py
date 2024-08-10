from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
    )

from django.utils.translation import gettext_lazy as _

from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage 
from rest_framework.decorators import api_view 
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response 
from django.db import connection 
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

#Below causes 'circular import' rn
#from .serializers import UserSerializer


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Added fields
    nameOnCard = models.CharField(_('name on card'), max_length=255, blank=True, null=True)
    cardNumber = models.CharField(_('card number'), max_length=16, blank=True, null=True)
    expiryDate = models.CharField(_('expiry date'), max_length=5, blank=True, null=True)  # Storing as MM/YY string
    cvc = models.CharField(_('CVC'), max_length=4, blank=True, null=True)  # Highly sensitive

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


# class CreditCardInfo(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
#     name_on_card = models.CharField(max_length=255)
#     card_number = models.CharField(max_length=20)  # Simplified; actual implementation may vary
#     expiry_date = models.CharField(max_length=5)  # Format: MM/YY
#     cvc = models.CharField(max_length=4)  # 3 or 4 digits depending on the card

#     def __str__(self):
#         return f"Card {self.card_number[-4:]} for {self.user.email}"


# Pech's backend Database
# Create your models here.
class GUITable(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(unique=True, max_length=50)
    unit = models.FloatField()
    price_per_unit = models.FloatField() 
    subtotal = models.FloatField()


class UnitType(models.Model): 
    unit_id = models.IntegerField()
    type = models.CharField(max_length=30) 

class ProductInfo(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(unique=True, max_length=50)
    unit_id = models.IntegerField()
    unit = models.FloatField()
    price_per_unit = models.FloatField() 



