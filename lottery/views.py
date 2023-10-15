from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import GTokenSerializer
from rest_framework.permissions import IsAuthenticated
from .models import GivenToken
from rest_framework.response import Response
from django.http import Http404

# Create your views here.

class GTokenAPIView(APIView):
    serializer_class = GTokenSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        data = GivenToken.objects.all()
        serializer = self.serializer_class(data, many=True)
        serialized_data =serializer.data
        return Response(serialized_data)
    
    def post(self, request, format=None):
        # print(request.data)
        serializer = self.serializer_class(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
        # serialized_data = None
            return Response(serialized_data)
        return Response(serializer.errors)