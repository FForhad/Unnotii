from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProductItemSerializer, ProductPointSerializer
from rest_framework.permissions import IsAuthenticated
from .models import ProductItem,ProductPoint
from rest_framework.response import Response
from django.http import Http404

# Create your views here.

class ProductItemAPIView(APIView):
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        data = ProductItem.objects.all()

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
    

class ProductItemsAIPView(APIView):
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self, pk):
        try:
            return ProductItem.objects.get(pk=pk)
        except ProductItem.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = self.serializer_class(self.get_object(pk))
        serialized_data = serializer.data
        return Response(serialized_data)
    
    def put(self, request, pk, format=None):
        Checklist = self.get_object(pk)
        serilaizer = self.serializer_class(Checklist, data = request.data, context={'request': request})
        if serilaizer.is_valid():
            serilaizer.save()
            serilaizer_data = serilaizer.data
            return Response(serilaizer_data)
        return Response(serilaizer.errors)
    def delete(self,request,pk, format =None):
        Checklist = self.get_object(pk)
        Checklist.delete()
        return Response(Http404)
    
class ProductPointAPIView(APIView):
    serializer_class = ProductPointSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        data = ProductPoint.objects.all()

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
    

class ProductPointsAIPView(APIView):
    serializer_class = ProductPointSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self, pk):
        try:
            return ProductPoint.objects.get(pk=pk)
        except ProductPoint.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = self.serializer_class(self.get_object(pk))
        serialized_data = serializer.data
        return Response(serialized_data)
    
    def put(self, request, pk, format=None):
        Checklist = self.get_object(pk)
        serilaizer = self.serializer_class(Checklist, data = request.data, context={'request': request})
        if serilaizer.is_valid():
            serilaizer.save()
            serilaizer_data = serilaizer.data
            return Response(serilaizer_data)
        return Response(serilaizer.errors)
    def delete(self,request,pk, format =None):
        Checklist = self.get_object(pk)
        Checklist.delete()
        return Response(Http404)
