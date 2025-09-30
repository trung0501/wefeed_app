# from django.shortcuts import render
# from rest_framework import viewsets
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.
# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

logger = logging.getLogger(__name__)

class ProjectCreateView(APIView):
    # Tạo project mới
    def post(self, request):
        logger.info("[PROJECT CREATE] Request received at %s", request.path)
        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                project = serializer.save(created_day=datetime.now())
                logger.info("Project created successfully: id=%s, name=%s",
                            project.id, getattr(project, "name", None))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning("Project creation failed. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error creating project")
            return Response({"error": f"Lỗi khi tạo project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectDetailView(APIView):
    # Lấy thông tin project
    def get(self, request, pk):
        logger.info("[PROJECT DETAIL] Request received at %s for project_id=%s", request.path, pk)
        try:
            project = get_object_or_404(Project, pk=pk)
            logger.info("Project found: id=%s, name=%s", project.id, project.name)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error retrieving project id=%s", pk)
            return Response({"error": f"Lỗi khi lấy project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Cập nhật project
    def put(self, request, pk):
        logger.info("[PROJECT UPDATE] Request received at %s for project_id=%s", request.path, pk)
        try:
            project = get_object_or_404(Project, pk=pk)
            logger.info("Project found: id=%s, name=%s", project.id, project.name)

            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                updated = serializer.save()
                logger.info("Project updated successfully: id=%s, new_data=%s",
                            updated.id, serializer.validated_data)
                return Response(
                    {"message": "Project đã được cập nhật thành công", **serializer.data},
                    status=status.HTTP_200_OK
                )

            logger.warning("Project update failed. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error updating project id=%s", pk)
            return Response({"error": f"Lỗi khi cập nhật project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Xóa project
    def delete(self, request, pk):
        logger.info("[PROJECT DELETE] Request received at %s for project_id=%s", request.path, pk)
        try:
            project = get_object_or_404(Project, pk=pk)
            project_name = project.name
            project.delete()
            logger.info("Project deleted successfully: id=%s, name=%s", pk, project_name)

            return Response({"message": f"Project '{project_name}' đã được xóa thành công"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception("Error deleting project id=%s", pk)
            return Response({"error": f"Lỗi khi xóa project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Phân trang
class ProjectListView(APIView):
    def get(self, request):
        logger.info("[PROJECT LIST] Request received at %s with query_params=%s",
                    request.path, request.query_params)
        try:
            projects = Project.objects.all().order_by("created_day")
            if not projects.exists():
                logger.warning("No projects found in database")
                return Response({"detail": "Không có project nào."},
                                status=status.HTTP_404_NOT_FOUND)

            paginator = PageNumberPagination()
            paginator.page_size = 5
            result_page = paginator.paginate_queryset(projects, request)

            serializer = ProjectSerializer(result_page, many=True)
            logger.info("Returning %s projects for page=%s",
                        len(result_page), request.query_params.get("page", 1))

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.exception("Error retrieving project list with pagination")
            return Response({"error": f"Lỗi khi lấy danh sách project: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
