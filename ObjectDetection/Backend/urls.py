"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls.resolvers import URLPattern
from backend import views

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 


urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('', include('backend.urls')),
    
    path('', views.HomePage, name='home'),
    path('guitable/', views.GUITableAPI),
    path('signup/', views.create_user, name='signup'),
    path('signin/', views.login_user, name='signin'),
    path('verify_cvc', views.verify_cvc),
    path('fetch_credit_card_info/', views.fetch_user_credit_card_info, name='fetch_credit_card_info'),
    # path('totalprice/', views.TotalPriceAPI),
    # path('objectdetection/', views.ObjectDetectionAPI),
    # path('productinfo/<int:pk>/', views.StudentAPI),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
