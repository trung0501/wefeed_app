# from django.shortcuts import render
import logging
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

logger = logging.getLogger(__name__)

# Tạo workspace mới
class WorkspaceCreateView(APIView):
    def post(self, request):
        logger.info("[WORKSPACE CREATE] Request received at %s", request.path)

        serializer = WorkspaceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            workspace = serializer.save()
            logger.info("Workspace created successfully: id=%s, name=%s", workspace.id, workspace.name)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning("Workspace creation failed. Errors: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Lấy, cập nhật, xóa workspace
class WorkspaceDetailView(APIView):
    def get(self, request, id):
        logger.info("[WORKSPACE DETAIL] Người dùng gửi yêu cầu tại %s với id=%s", request.path, id)
        try:
            workspace = get_object_or_404(Workspace, id=id)
            logger.info("Tìm thấy workspace: id=%s, name=%s", workspace.id, workspace.name)

            serializer = WorkspaceSerializer(workspace)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Lỗi truy xuất workspace id=%s", id)
            return Response(
                {"error": f"Lỗi khi lấy workspace: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, id):
        logger.info("[WORKSPACE UPDATE] Người dùng gửi yêu cầu tại %s với id=%s", request.path, id)
        try:
            workspace = get_object_or_404(Workspace, id=id)
            logger.info("Tìm thấy workspace: id=%s, name=%s", workspace.id, workspace.name)

            serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
            if serializer.is_valid():
                updated = serializer.save()
                logger.info("Cập nhật workspace thành công: id=%s, name=%s", updated.id, updated.name)
                return Response(serializer.data, status=status.HTTP_200_OK)

            logger.warning("Cập nhật workspace thất bại. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Lỗi khi cập nhật workspace id=%s", id)
            return Response(
                {"error": f"Lỗi khi cập nhật workspace: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def delete(self, request, id):
        logger.info("[WORKSPACE DELETE] Người dùng gửi yêu cầu tại %s với id=%s", request.path, id)
        try:
            workspace = get_object_or_404(Workspace, id=id)
            logger.info("Tìm thấy workspace: id=%s, name=%s", workspace.id, workspace.name)

            workspace_name = workspace.name
            workspace.delete()
            logger.info("Xóa workspace thành công: id=%s, name=%s", id, workspace_name)

            return Response(
                {"message": f"Workspace {workspace_name} đã được xóa thành công."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            logger.exception("Lỗi khi xóa workspace id=%s", id)
            return Response(
                {"error": f"Lỗi khi xóa workspace: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Nâng cấp gói subscription
class WorkspaceUpgradeView(APIView):
    def put(self, request, id):
        logger.info("[WORKSPACE UPGRADE] Người dùng gửi yêu cầu tại %s với id=%s", request.path, id)
        try:
            workspace = get_object_or_404(Workspace, id=id)
            logger.info("Tìm thấy workspace: id=%s, name=%s, current_plan=%s",
                        workspace.id, workspace.name, getattr(workspace, "subscription_plan", None))

            plan = request.data.get("subscription_plan")
            logger.debug("Yêu cầu kế hoạch: %s", plan)

            if plan is None:
                logger.warning("Missing subscription_plan in request body")
                return Response({"error": "Thiếu trường subscription_plan"}, status=status.HTTP_400_BAD_REQUEST)

            # Normalize input
            normalized_plan = str(plan).strip().title()
            allowed_plans = {"Free", "Pro", "Enterprise"}
            logger.debug("Normalized plan: %s; Allowed: %s", normalized_plan, allowed_plans)

            if normalized_plan not in allowed_plans:
                logger.warning("Invalid plan: %s", normalized_plan)
                return Response({"error": "Gói không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

            # Optional: prevent redundant update
            if getattr(workspace, "subscription_plan", None) == normalized_plan:
                logger.info("ℹPlan unchanged: already %s", normalized_plan)
                return Response({"message": f"Gói đã là {normalized_plan}, không cần nâng cấp"},
                                status=status.HTTP_200_OK)

            workspace.subscription_plan = normalized_plan
            workspace.save()
            logger.info("Workspace upgraded: id=%s, name=%s, new_plan=%s",
                        workspace.id, workspace.name, normalized_plan)

            return Response({"message": f"Đã nâng cấp lên {normalized_plan}"},
                            status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Error upgrading workspace id=%s", id)
            return Response({"error": f"Lỗi khi nâng cấp gói: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)