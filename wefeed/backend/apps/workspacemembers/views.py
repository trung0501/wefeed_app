# from django.shortcuts import render
# from rest_framework import viewsets
import logging
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

logger = logging.getLogger(__name__)

class WorkspaceMemberListCreateView(APIView):
    def get(self, request, id):
        logger.info("[WORKSPACE MEMBER LIST] Request received at %s for workspace_id=%s", request.path, id)
        try:
            members = WorkspaceMember.objects.filter(workspace_id=id)
            logger.info("Found %s members in workspace_id=%s", members.count(), id)

            serializer = WorkspaceMemberSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error retrieving members for workspace_id=%s", id)
            return Response({"error": f"Lỗi khi lấy danh sách thành viên: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, id):
        logger.info("[WORKSPACE MEMBER CREATE] Request received at %s for workspace_id=%s", request.path, id)
        try:
            workspace = get_object_or_404(Workspace, pk=id)
            logger.info("Workspace found: id=%s, name=%s", workspace.id, workspace.name)

            data = request.data.copy()
            data["workspace"] = workspace.id
            data["joined_day"] = datetime.now()

            serializer = WorkspaceMemberSerializer(data=data)
            if serializer.is_valid():
                member = serializer.save()
                logger.info("Member added: id=%s, user=%s, workspace_id=%s",
                            member.id, getattr(member, "user_id", None), workspace.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning("Failed to add member. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error adding member to workspace_id=%s", id)
            return Response({"error": f"Lỗi khi thêm thành viên: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        logger.info("[MEMBER UPDATE] Request received at %s for workspace_id=%s",
                    request.path, id)
        try:
            member = get_object_or_404(WorkspaceMember, workspace_id=id)
            logger.info("Member found: id=%s, user_id=%s, current_role=%s",
                        member.id, member.user_id, member.role)

            serializer = WorkspaceMemberSerializer(member, data=request.data, partial=True)
            if serializer.is_valid():
                updated = serializer.save()
                logger.info("Member updated successfully: id=%s, user_id=%s, new_data=%s",
                            updated.id, updated.user_id, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            logger.warning("Member update failed. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error updating member_id=%s in workspace_id=%s", id)
            return Response({"error": f"Lỗi khi cập nhật thành viên: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

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
