import random
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, OTP
from .serializers import CustomUserSerializer, OTPSerializer
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.utils import timezone

@api_view(['POST'])
def register_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    if not phone_number or not password:
        return Response({'error': 'Phone number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    otp = str(random.randint(100000, 999999))
    sms_url = f'http://bulksmsbd.net/api/smsapi?api_key=YOUR_API_KEY&type=text&number={phone_number}&message=Your OTP is {otp}.'
    response = requests.get(sms_url)

    if response.status_code == 200:
        user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
        user.password = make_password(password)
        user.save()

        expiry_time = timezone.now() + timedelta(minutes=10)
        OTP.objects.update_or_create(user=user, defaults={'otp': otp, 'expiry': expiry_time})

        return Response({'message': 'OTP sent successfully and user registered.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Failed to send OTP via SMS.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data.get('phone_number')
    otp_entered = request.data.get('otp')

    try:
        user = CustomUser.objects.get(phone_number=phone_number)
        otp_record = OTP.objects.filter(user=user, otp=otp_entered).first()

        if not otp_record:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() > otp_record.expiry:
            otp_record.delete()
            return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        otp_record.delete()

        return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
