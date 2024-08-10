from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UnitType, ProductInfo, GUITable, CustomUserManager, CustomUser

admin.site.register(CustomUser)
admin.site.register(GUITable)
admin.site.register(UnitType)
admin.site.register(ProductInfo)