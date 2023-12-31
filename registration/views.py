import requests
import random
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token

# Define your SMS API URL with placeholders for RECEIVER_PHONE_NUMBER and MESSAGE_CONTENT
# SMS_API_URL_TEMPLATE = "http://bulksmsbd.net/api/smsapi?api_key=drr6oD1PnMwW6WhuPNbV&type=text&number={}&senderid=8809617613176&message={}"
# SMS_API_URL_TEMPLATE = "https://login.dianasms.com/api/v3/sms/send?api_key=224|mNinL0Koe9WLLIZDbFT9VgQsd2OaZDmUL5UlkXVF&type=text&number={}&senderid=8809601003664&message={}"
# not working
# SMS_API_URL_TEMPLATE = "https://login.esms.com.bd/api/v3/sms/send"
# SMS_API_URL_TEMPLATE = "https://login.dianasms.com/api/v3/sms/send"

# @api_view(['POST'])
# def register_user(request):
#     phone_number = request.data.get('phone_number')
#     password = request.data.get('password')

#     if not phone_number or not password:
#         return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if UserProfile.objects.filter(phone_number=phone_number).exists():
#         return Response({'error': 'User with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

#     # Generate OTP
#     otp = ''.join(random.choices('0123456789', k=6))
#     otp_expiration = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes

#     # Send OTP via SMS API
#     sms_params = {
#         'recipient': phone_number,
#         'sender_id': '8809601003664',
#         'type': 'plain',
#         'message': f'Your OTP is {otp}'
#     }

#     # You may need to set the Authorization header based on your specific API key
#     headers = {
#         'Authorization': 'Bearer 224|mNinL0Koe9WLLIZDbFT9VgQsd2OaZDmUL5UlkXVF'
#     }

#     response = requests.post(SMS_API_URL_TEMPLATE, data=sms_params, headers=headers)

#     if response.status_code != 200:
#         return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     # Create the user profile
#     user_profile = UserProfile(
#         phone_number=phone_number,
#         otp=otp,
#         otp_expiration=otp_expiration
#     )
#     user_profile.set_password(password)
#     user_profile.save()

#     serializer = UserProfileSerializer(user_profile)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def register_user(request):
#     phone_number = request.data.get('phone_number')
#     password = request.data.get('password')

#     if not phone_number or not password:
#         return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if UserProfile.objects.filter(phone_number=phone_number).exists():
#         return Response({'error': 'User with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

#     # Generate OTP
#     otp = ''.join(random.choices('0123456789', k=6))
#     otp_expiration = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes

#     # Send OTP via SMS API
#     sms_api_url = SMS_API_URL_TEMPLATE.format(phone_number, f'Your OTP is {otp}')
#     response = requests.get(sms_api_url)

#     if response.status_code != 200:
#         return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     # Create the user profile
#     user_profile = UserProfile(
#         phone_number=phone_number,
#         # password=password,
#         otp=otp,
#         otp_expiration=otp_expiration
#     )
#     user_profile.set_password(password)
#     user_profile.save()

#     serializer = UserProfileSerializer(user_profile)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


greenweburl = "http://api.greenweb.com.bd/api.php"
token = "10208204959169824539951b0b11f7c471a0eafdeb86a4e8d9d90"

@api_view(['POST'])
def register_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone_number or not password:
        return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'User with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

    otp = ''.join(random.choices('0123456789', k=6))
    otp_expiration = timezone.now() + timedelta(minutes=10)

    # Send OTP via GreenWeb SMS API
    to = f'{phone_number}'  # Format the phone number as per GreenWeb's requirement
    message = f'Your OTP is {otp}'

    data = {
        'token': token,
        'to': to,
        'message': message
    }

    response = requests.post(url=greenweburl, data=data)

    if response.status_code != 200:
        return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user_profile = UserProfile(
        phone_number=phone_number,
        otp=otp,
        otp_expiration=otp_expiration
    )
    user_profile.set_password(password)
    user_profile.save()

    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data.get('phone_number')
    user_input_otp = request.data.get('otp')

    if not user_input_otp:
        return Response({'error': 'OTP is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_profile = UserProfile.objects.get(phone_number=phone_number)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if OTP is expired
    if user_profile.otp_expiration < timezone.now():
        return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify OTP
    if user_input_otp == user_profile.otp:
        user_profile.otp_verified = True
        user_profile.save()
        serializer = UserProfileSerializer(user_profile)
        return Response({'message': 'OTP verified', 'user_profile': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        # This uses the custom backend you've added.
        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                # User is not active, need approval from admin
                return Response({'error': 'Account is not active. Need approval from admin.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Print debugging information
            print(f"Failed to authenticate user with phone_number: {phone_number} and password: {password}")
            return Response({'error': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
