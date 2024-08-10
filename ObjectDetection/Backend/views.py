from django.shortcuts import render
import json


from backend.models import GUITable 
from backend.serializers import GUITableSerializer
from .models import CustomUser
from backend.utitilies import modifyTable

from django.contrib.auth.decorators import login_required  

from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage 

from rest_framework.response import Response 
from django.db import connection 
from django.views.decorators.http import require_http_methods

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# from .serializers import CreditCardInfoSerializer
# from .models import CreditCardInfo

# Create your views here.
@csrf_exempt
def GUITableAPI(request, pk=0):
    # if there is a request to get a data
    if request.method == 'GET':
        # Call the insert/remove here (autofetch from the frontend)
        modifyTable()
        inCart = GUITable.objects.all() # get all data
        inCart_serializer = GUITableSerializer(inCart, many=True) # serialize the data
        return JsonResponse(inCart_serializer.data, safe=False) # return Json file 
    return; 




def HomePage(request):
    return render(request, 'backend/home.html')



# @csrf_exempt
# @require_http_methods(["POST"])
# def create_user(request):
#     data = JSONParser().parse(request)
#     serializer = UserSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()  # The user object with payment information is created here
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    
    data = JSONParser().parse(request)
    print("hello!!")
    print(data)
    email = data.get('email')  # 'email' is used as 'username' in CustomUser model

    password = data.get('password')
    user = authenticate(email=email, password=password)  # authenticate using 'email'
    print(user)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key}, status=status.HTTP_200_OK)
    return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def setup_payment(request):
#     data = JSONParser().parse(request)
#     data['user'] = request.user.pk
#     serializer = CreditCardInfoSerializer(data=data)
#     if serializer.is_valid():
#         # Set the user from the request
#         serializer.save(user=request.user)
#         return JsonResponse({'message': 'Payment setup successful'}, status=200)
#     else:
#         return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def verify_cvc(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_credit_card_info = data.get('userCreditCardInfo', {})
            cvc = data.get('cvc', '')
            
            # Assuming you have a function to verify CVC
            # Replace this with your actual implementation
            cvc_verified = verify_cvc_function(user_credit_card_info, cvc)
            
            if cvc_verified:
                return JsonResponse({'message': 'CVC verified'}, status=200)
            else:
                print(cvc) # the CVC is correct from the frontend
                print(user_credit_card_info) # this shit is empty
                return JsonResponse({'error': 'CVC does not match'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def verify_cvc_function(user_credit_card_info, cvc):
    # Extract necessary info from user_credit_card_info
    card_number = user_credit_card_info.get('cardNumber')
    expiry_date = user_credit_card_info.get('expiryDate')

    try:
        # Retrieve the user based on the card number and expiry date
        # Note: Adjust the query based on how your model relations are set up
        user = CustomUser.objects.get(cardNumber=card_number, expiryDate=expiry_date)
        
        # Verify CVC
        return user.cvc == cvc
    except CustomUser.DoesNotExist:
        # Handle case where the user or card info does not exist
        return False

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_credit_card_info(request):
    # Assuming the request.user is the authenticated user
    user = request.user
    if user:
        credit_card_info = {
            'nameOnCard': user.nameOnCard,
            'cardNumber': user.cardNumber,
            'expiryDate': user.expiryDate,
        }
        return JsonResponse(credit_card_info, status=200)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)