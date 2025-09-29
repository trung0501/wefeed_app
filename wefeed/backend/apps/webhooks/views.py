# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Webhook
from .serializers import WebhookSerializer
import requests

# Create your views here.
# class WebhookViewSet(viewsets.ModelViewSet):
#     queryset = Webhook.objects.all()
#     serializer_class = WebhookSerializer

# Đăng ký webhook mới 
class WebhookCreateView(APIView):
    def post(self, request):
        serializer = WebhookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_day=datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy, cập nhật, xóa webhook 
class WebhookDetailView(APIView):
    # Lấy thông tin webhook
    def get(self, request, id):
        webhook = get_object_or_404(Webhook, id=id)
        serializer = WebhookSerializer(webhook)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Cập nhật webhook
    def put(self, request, id):
        webhook = get_object_or_404(Webhook, id=id)
        serializer = WebhookSerializer(webhook, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_day=datetime.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa webhook
    def delete(self, request, id):
        webhook = get_object_or_404(Webhook, id=id)
        webhook.delete()
        return Response({'message': 'Đã xóa webhook'}, status=status.HTTP_204_NO_CONTENT)

# Gửi dữ liệu sự kiện đến endpoint đã đăng
class EventSendView(APIView):
    def post(self, request):
        event_data = request.data
        # Lấy tất cả webhook đang active
        # webhooks = Webhook.objects.filter(active=True)
        webhooks = Webhook.objects.all()
        results = []
        for webhook in webhooks:
            try:
                resp = requests.post(webhook.endpoint_url, json=event_data, timeout=5)
                results.append({
                    'webhook_id': webhook.id,
                    'status_code': resp.status_code,
                    'response': resp.text
                })
            except Exception as e:
                results.append({
                    'webhook_id': webhook.id,
                    'error': str(e)
                })
        return Response({'results': results}, status=status.HTTP_200_OK)
