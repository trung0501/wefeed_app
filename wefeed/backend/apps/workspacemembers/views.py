# from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Workspace, WorkspaceMember, User
from .serializers import WorkspaceMemberSerializer

# Create your views here.
# class WorkspaceMemberViewSet(viewsets.ModelViewSet):
#     queryset = WorkspaceMember.objects.all()
#     serializer_class = WorkspaceMemberSerializer

class WorkspaceMemberListCreateView(APIView):
    def get(self, request, id):
        members = WorkspaceMember.objects.filter(workspace_id=id)
        serializer = WorkspaceMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        workspace = get_object_or_404(Workspace, id=id)
        data = request.data.copy()

        # Gắn workspace và ngày tham gia
        data["workspace"] = workspace.id
        data["joined_day"] = datetime.now()

        serializer = WorkspaceMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WorkspaceMemberRoleUpdateView(APIView):
    # Phân quyền thành viên 
    def put(self, request, id, userId):
        member = get_object_or_404(WorkspaceMember, workspace_id=id, user_id=userId)
        role = request.data.get('role')
        if role not in ['Owner', 'Admin', 'Member']:
            return Response({'error': 'Vai trò không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        member.role = role
        member.save()
        return Response({'message': f'Đã cập nhật vai trò thành {role}'}, status=status.HTTP_200_OK)

class WorkspaceMemberDeleteView(APIView):
    # Xóa thành viên
    def delete(self, request, id, userId):
        member = get_object_or_404(WorkspaceMember, workspace_id=id, user_id=userId)
        member.delete()
        return Response({'message': 'Đã xóa thành viên'}, status=status.HTTP_204_NO_CONTENT)
