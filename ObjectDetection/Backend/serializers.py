from rest_framework import fields, serializers 
from .models import GUITable, CustomUser,CustomUserManager
from django.contrib.auth import get_user_model
from rest_framework import fields, serializers


# this is where the data is received back 
class GUITableSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GUITable
        fields = (
                'product_id',
                'product_name',
                'unit',
                'price_per_unit',
                'subtotal')

# class TotalPriceSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = TotalPrice
#         fields = ('subtotal')



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'nameOnCard', 'cardNumber', 'expiryDate', 'cvc')
        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'required': True},
            'nameOnCard': {'required': False},  # Assuming not required for user creation
            'cardNumber': {'required': False, 'write_only': True},
            'expiryDate': {'required': False, 'write_only': True},
            'cvc': {'required': False, 'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),  # Default to empty string if 'name' is not provided
            nameOnCard=validated_data.get('nameOnCard', ''),
            cardNumber=validated_data.get('cardNumber', ''),
            expiryDate=validated_data.get('expiryDate', ''),
            cvc=validated_data.get('cvc', ''),
        )

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


# class CreditCardInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreditCardInfo
#         fields = ('user', 'name_on_card', 'card_number', 'expiry_date', 'cvc')
#         extra_kwargs = {
#             'user': {'read_only': True},  # Prevent manual setting of the user field
#         }