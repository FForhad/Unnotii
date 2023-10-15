from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProfileSerializer, RechargeLogSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Profile, RechargeLog
from rest_framework.response import Response
from django.http import Http404

class ProfileAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"detail": "Profile not found for the authenticated user."}, status=404)
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ProfilesAIPView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = self.serializer_class(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = self.serializer_class(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Create a RechargeLog entry if points were updated.
            if 'points' in request.data:
                RechargeLog.objects.create(user=request.user, key="Recharge", value=request.data['points'])
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=204)  # Return HTTP 204 No Content status.


class RechargeLogAPIView(APIView):
    serializer_class = RechargeLogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Filter logs by the authenticated user
        logs = RechargeLog.objects.filter(user=request.user)
        serializer = self.serializer_class(logs, many=True)
        return Response(serializer.data)