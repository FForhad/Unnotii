from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Code, CodePDF
import io
from reportlab.pdfgen import canvas
from django.core.files import File
from django.utils import timezone
from .serializers import RechargeSerializer, PaidPointSerializer
from userprofile.models import Profile
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()


class CodeAddView(APIView):
    
    def post(self, request):
        num_of_code = int(request.data.get('num_of_code'))
        value_of_code = request.data.get('value_of_code')

        with open('uc.txt', 'r') as file:
            lines = file.readlines()

        lines_to_delete = []
        new_codes = []

        for line in lines[:num_of_code]:
            line = line.strip()
            if line:
                new_codes.append((line, value_of_code))
                lines_to_delete.append(line)
        
        # Saving the codes to the database
        Code.objects.bulk_create([Code(key=k, value=v) for k, v in new_codes])

        # Updating the uc.txt file
        with open('uc.txt', 'w') as file:
            file.writelines(lines[len(lines_to_delete):])

        # Creating a simple PDF with the keys
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        y_position = 800  # start from the top of the page
        for key, _ in new_codes:
            p.drawString(100, y_position, key)
            y_position -= 14
        p.showPage()
        p.save()

        # Save PDF to the database
        buffer.seek(0)
        pdf_file = CodePDF(pdf=File(buffer, name="codes_{}.pdf".format(timezone.now().strftime('%Y%m%d_%H%M%S'))))
        pdf_file.save()

        # Return the PDF to the user
        return FileResponse(buffer, as_attachment=True, filename=pdf_file.pdf.name)
    


class RechargeAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = RechargeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dial_code = serializer.validated_data['dial_code']

        # Check if the provided dial_code exists in the Code model
        try:
            code_obj = Code.objects.get(key=dial_code)
        except Code.DoesNotExist:
            return Response({'message': 'Invalid Recharge number'}, status=status.HTTP_400_BAD_REQUEST)

        # If dial_code is found, update the user's profile points
        try:
            user_profile = Profile.objects.get(user=request.user)
            user_profile.points += code_obj.value
            user_profile.save()
            # After successful recharge, remove the dial_code from Code model
            code_obj.delete()
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': f'Recharge successful! User points: {user_profile.points}'}, status=status.HTTP_200_OK)



class PaidPointView(APIView):
    serializer_class = PaidPointSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            point_to_pay = serializer.validated_data['point']

            try:
                user = User.objects.get(phone_number=phone_number)  # Assuming phone_number is saved as username in your User model
                profile = Profile.objects.get(user=user)
                
                if profile.points >= point_to_pay:
                    profile.points -= point_to_pay
                    profile.save()
                    return Response({'message': f"Points paid successfully! User points: {profile.points}"}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Entered value exceeds the user points.'}, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response({'error': 'User with provided phone number does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)