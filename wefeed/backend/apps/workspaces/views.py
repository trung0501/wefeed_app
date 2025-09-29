# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Workspace
from .serializers import WorkspaceSerializer

# Create your views here.
# class WorkspaceViewSet(viewsets.ModelViewSet):
#     queryset = Workspace.objects.all()
#     serializer_class = WorkspaceSerializer

# Tạo workspace mới
class WorkspaceCreateView(APIView):
    def post(self, request):
        serializer = WorkspaceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save                   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Lấy, cập nhật, xóa workspace
class WorkspaceDetailView(APIView):
    def get(self, request, id):
        try:
            workspace = get_object_or_404(Workspace, id=id)
            serializer = WorkspaceSerializer(workspace)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Lỗi khi lấy workspace: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, id):
        try:
            workspace = get_object_or_404(Workspace, id=id)
            serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Lỗi khi cập nhật workspace: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def delete(self, request, id):
        try:
            workspace = get_object_or_404(Workspace, id=id)
            workspace.delete()
            return Response(
                {"message": f"Workspace '{workspace.name}' đã được xóa thành công."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": f"Lỗi khi xóa workspace: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Nâng cấp gói subscription
class WorkspaceUpgradeView(APIView):
    def put(self, request, id):
        workspace = get_object_or_404(Workspace, id=id)
        plan = request.data.get('subscription_plan')
        if plan not in ['Free', 'Pro', 'Enterprise']:
            return Response({'error': 'Gói không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        workspace.subscription_plan = plan
        workspace.save()
        return Response({'message': f'Đã nâng cấp lên {plan}'}, status=status.HTTP_200_OK)
