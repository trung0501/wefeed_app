# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Canvas
from .serializers import CanvasSerializer

# Create your views here.
# class CanvasViewSet(viewsets.ModelViewSet):
#     queryset = Canvas.objects.all()
#     serializer_class = CanvasSerializer

class CanvasCreateView(APIView):
    # Tạo canvas mới
    def post(self, request):
        serializer = CanvasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_day=datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CanvasDetailView(APIView):
    # Lấy thông tin canvas
    def get(self, request, id):
        canvas = get_object_or_404(Canvas, id=id)
        serializer = CanvasSerializer(canvas)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Cập nhật canvas
    def put(self, request, id):
        canvas = get_object_or_404(Canvas, id=id)
        serializer = CanvasSerializer(canvas, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Xóa canvas
    def delete(self, request, id):
        canvas = get_object_or_404(Canvas, id=id)
        canvas.delete()
        return Response({'message': 'Đã xóa canvas'}, status=status.HTTP_204_NO_CONTENT)