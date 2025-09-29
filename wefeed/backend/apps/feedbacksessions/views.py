# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import FeedbackSession
from apps.canvas.models import Canvas
from .serializers import FeedbackSessionSerializer

# Create your views here
# class FeedbackSessionViewSet(viewsets.ModelViewSet):
#     queryset = FeedbackSession.objects.all()
#     serializer_class = FeedbackSessionSerializer

# Tạo phiên phản hồi 
class FeedbackSessionCreateView(APIView):
    def post(self, request):
        serializer = FeedbackSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_day=datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy thông tin một phiên phản hồi 
class FeedbackSessionDetailView(APIView):
    def get(self, request, id):
        session = get_object_or_404(FeedbackSession, id=id)
        serializer = FeedbackSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        session = get_object_or_404(FeedbackSession, id=id)
        serializer = FeedbackSessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        session = get_object_or_404(FeedbackSession, id=id)
        session.delete()
        return Response({'message': 'Đã xóa phiên phản hồi'}, status=status.HTTP_204_NO_CONTENT)

# Lấy tất cả phiên của một project 
class ProjectFeedbackSessionListView(APIView):
    def get(self, request, id):
        # Lấy tất cả canvas thuộc project có id = id
        canvas_ids = Canvas.objects.filter(project_id=id).values_list('id', flat=True)

        # Lấy tất cả phiên phản hồi thuộc các canvas đó
        sessions = FeedbackSession.objects.filter(canvas_id__in=canvas_ids)

        serializer = FeedbackSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)