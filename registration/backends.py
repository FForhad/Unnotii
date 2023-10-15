# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None
